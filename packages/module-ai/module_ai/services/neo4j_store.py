import logging

from cortex_core.settings import get_settings
from module_ai.schemas import LawNodeResponse
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

SEED_LAWS = [
    {
        "ref": "stgb-146",
        "title": "Schweizerisches Strafgesetzbuch",
        "article": "Art. 146 Betrug",
        "content": (
            "Wer in der Absicht, sich oder einen Dritten unrechtmässig zu bereichern, "
            "durch Täuschung oder arglistige Täuschung des Irrtums eines andern "
            "fremdes Vermögen schädigt, wird mit Freiheitsstrafe bis zu fünf Jahren "
            "oder Geldstrafe bestraft."
        ),
        "valid_from": "2020-01-01",
    },
    {
        "ref": "or-41",
        "title": "Obligationenrecht",
        "article": "Art. 41 Schadenersatz",
        "content": (
            "Wer unrichtig, unsorgfältig oder in Übertretung vertraglicher oder "
            "gesetzlicher Pflichten einen Schaden verursacht, haftet dem Geschädigten "
            "für dessen Behebung."
        ),
        "valid_from": "2020-01-01",
    },
    {
        "ref": "zpo-80",
        "title": "Zivilprozessordnung",
        "article": "Art. 80 Beweis",
        "content": (
            "Das Gericht würdigt die Beweise nach der freien Überzeugung. "
            "Es darf Beweismittel nur berücksichtigen, die rechtsgültig erhoben worden sind."
        ),
        "valid_from": "2020-01-01",
    },
]


def _get_driver():
    settings = get_settings()
    return GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )


def seed_laws_if_empty() -> int:
    driver = _get_driver()
    try:
        with driver.session() as session:
            count = session.run("MATCH (l:Law) RETURN count(l) AS c").single()["c"]
            if count > 0:
                return 0

            for law in SEED_LAWS:
                session.run(
                    """
                    MERGE (l:Law {ref: $ref})
                    SET l.title = $title,
                        l.article = $article,
                        l.content = $content,
                        l.valid_from = $valid_from
                    """,
                    **law,
                )
            logger.info("Seeded %d law nodes in Neo4j", len(SEED_LAWS))
            return len(SEED_LAWS)
    finally:
        driver.close()


def get_law_by_ref(law_ref: str) -> LawNodeResponse | None:
    driver = _get_driver()
    try:
        with driver.session() as session:
            record = session.run(
                """
                MATCH (l:Law {ref: $ref})
                RETURN l.ref AS ref, l.title AS title, l.article AS article,
                       l.content AS content, l.valid_from AS valid_from,
                       l.valid_to AS valid_to
                """,
                ref=law_ref,
            ).single()

            if not record:
                return None

            valid_from = record["valid_from"]
            if hasattr(valid_from, "isoformat"):
                valid_from = valid_from.isoformat()

            valid_to = record["valid_to"]
            if valid_to and hasattr(valid_to, "isoformat"):
                valid_to = valid_to.isoformat()

            return LawNodeResponse(
                ref=record["ref"],
                title=record["title"],
                article=record["article"],
                content=record["content"],
                valid_from=str(valid_from),
                valid_to=str(valid_to) if valid_to else None,
            )
    finally:
        driver.close()


def ping_neo4j() -> bool:
    driver = _get_driver()
    try:
        driver.verify_connectivity()
        return True
    except Exception:
        return False
    finally:
        driver.close()
