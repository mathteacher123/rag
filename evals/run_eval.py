import json
import os
import math
from datetime import UTC, datetime
from pathlib import Path

from llama_index.core import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine

from ragas import evaluate
from ragas.dataset_schema import EvaluationDataset, SingleTurnSample
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.llms import llm_factory
from ragas.metrics import (
    AnswerCorrectness,
    AnswerRelevancy,
    context_precision,
    ContextRecall,
    Faithfulness,
)

from app.core.config import settings
from app.services.rag.embedding import embed_model
from app.services.rag.engine import retriever, text_qa_template, query_engine
from app.services.rag.llm import llm

from langchain_openai import ChatOpenAI
from google.genai import types
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from openai import OpenAI
from llama_index.llms.openai_like import OpenAILike

DATASET_PATH = Path("evals/dataset.jsonl")


def load_rows() -> list[dict]:
    with DATASET_PATH.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def build_eval_engine() -> RetrieverQueryEngine:
    llm2 = OpenAILike(
        api_key=os.environ.get("FREELLMAPI_API_KEY"),
        api_base="http://localhost:3001/v1",
        model="auto:intelligence",
        is_chat_model=True
    )
    # return query_engine
    response_synthesizer = get_response_synthesizer(
        llm=llm2,
        streaming=False,
        text_qa_template=text_qa_template,
    )
    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )


def collect_samples(engine: RetrieverQueryEngine) -> tuple[list, int, list]:
    samples = []
    empty_context_count = 0
    error_rows = []

    for index, row in enumerate(load_rows()):
        question = row.get("question")
        try:
            response = engine.query(question)
            answer = str(response.response)
            contexts = [node.get_content() for node in response.source_nodes]
        except Exception as exc:  # noqa: BLE001
            answer = ""
            contexts = []
            error_rows.append({"index": index, "question": question, "error": str(exc)})

        if not contexts:
            empty_context_count += 1

        samples.append(
            SingleTurnSample(
                user_input=question,
                response=answer,
                retrieved_contexts=contexts,
                reference=row.get("ground_truth"),
            )
        )
        """
        # Print statements to debug and inspect your evaluation inputs
        print("\n--- EVALUATION SAMPLE LOG ---")
        print(f"User Input (Question): {question}")
        print(f"Response (Answer):     {answer}")
        print(f"Retrieved Contexts:    {contexts}")
        print(f"Reference (Truth):     {row.get('ground_truth')}")
        print("-" * 30)
        """
        break

    return samples, empty_context_count, error_rows


def metric_means(scores: list[dict]) -> dict[str, float | None]:
    if not scores:
        return {}
    means = {}
    for name in scores[0]:
        values = [
            row[name]
            for row in scores
            if isinstance(row.get(name), int | float) and not math.isnan(row[name])
        ]
        means[name] = sum(values) / len(values) if values else None
    return means


def main() -> None:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"{DATASET_PATH} not found. Run `python -m evals.generate_dataset` first."
        )

    engine = build_eval_engine()
    samples, empty_context_count, error_rows = collect_samples(engine)

    judge_llm = OpenAI(
        api_key=os.environ.get("FREELLMAPI_API_KEY"),
        base_url="http://localhost:3001/v1",
    )

    ragas_llm = llm_factory(
        model="auto:intelligence", 
        provider="openai", 
        client=judge_llm
    )

    """
    judge_embed = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", # Ensure the base model string is exact
        api_key=settings.GEMINI_API_KEY,
        # Map your production dimension rules here
        output_dimensionality=settings.EMBEDDING_DIM 
    )
    """
    
    #context_precision.llm = ragas_llm
    result = evaluate(
        dataset=EvaluationDataset(samples=samples),
        metrics=[
            context_precision,
            #ContextRecall(llm=ragas_llm),
            #Faithfulness(llm=ragas_llm),
            #AnswerRelevancy(llm=ragas_llm),
            #AnswerCorrectness(llm=ragas_llm),
        ],
        llm=ragas_llm,
        # embeddings=LangchainEmbeddingsWrapper(embe),
        raise_exceptions=False,
        show_progress=True,
    )

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    report_dir = Path(settings.EVAL_REPORT_DIR) / timestamp
    report_dir.mkdir(parents=True, exist_ok=True)

    result.to_pandas().to_csv(report_dir / "rows.csv", index=False)

    summary = {
        "timestamp": timestamp,
        "metric_means": metric_means(result.scores),
        "empty_context_count": empty_context_count,
        "error_rows": error_rows,
        "sample_count": len(samples),
        "config": {
            "judge_model": settings.EVAL_JUDGE_MODEL,
            "testset_size": settings.EVAL_TESTSET_SIZE,
            "llm_model": settings.LLM_MODEL,
            "embedding_model": settings.EMBEDDING_MODEL,
            "retrieval_top_k": settings.RETRIEVAL_TOP_K,
            "retrieval_similarity_cutoff": settings.RETRIEVAL_SIMILARITY_CUTOFF,
        },
    }
    with (report_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(f"Report written to {report_dir}")


if __name__ == "__main__":
    main()
