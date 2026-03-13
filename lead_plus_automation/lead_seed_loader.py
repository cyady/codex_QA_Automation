from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


def parse_optional_int(value: str) -> Optional[int]:
    value = (value or "").strip()
    if value == "":
        return None
    return int(value)


def parse_optional_str(value: str) -> Optional[str]:
    value = (value or "").strip()
    return value if value else None


def parse_bool(value: str) -> bool:
    value = (value or "").strip().lower()
    return value in {"true", "1", "yes", "y"}


def parse_bool_with_default(value: str, default: bool) -> bool:
    value = (value or "").strip()
    if value == "":
        return default
    return parse_bool(value)


def parse_raw_str(value: str) -> str:
    return (value or "").strip()


@dataclass(frozen=True)
class LeadSeedRecord:
    case_id: str
    title: str
    full_name: str
    email: str
    phone: Optional[str]
    mobile: Optional[str]
    company_name: Optional[str]
    job_title: Optional[str]
    department: Optional[str]
    country: Optional[str]
    city: Optional[str]
    industry: Optional[str]
    company_size: Optional[str]
    revenue_krw: Optional[int]
    website: Optional[str]
    owner: Optional[str]
    lead_status: Optional[str]
    lifecycle_stage: Optional[str]
    score: Optional[int]
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    last_activity_date: Optional[str]
    amount_krw: Optional[int]
    created_date: Optional[str]
    consent_status: Optional[str]
    expected_dynamic_match: bool
    notes: Optional[str]
    automation_enabled: bool
    priority: Optional[str]
    expected_create_success: bool
    expected_fail_reason: Optional[str]
    title_override: str
    title_should_be_valid: bool
    company_select_text: Optional[str]
    contact_select_text: Optional[str]

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> "LeadSeedRecord":
        return cls(
            case_id=row["case_id"].strip(),
            title=row["title"].strip(),
            full_name=row["full_name"].strip(),
            email=row["email"].strip(),
            phone=parse_optional_str(row.get("phone", "")),
            mobile=parse_optional_str(row.get("mobile", "")),
            company_name=parse_optional_str(row.get("company_name", "")),
            job_title=parse_optional_str(row.get("job_title", "")),
            department=parse_optional_str(row.get("department", "")),
            country=parse_optional_str(row.get("country", "")),
            city=parse_optional_str(row.get("city", "")),
            industry=parse_optional_str(row.get("industry", "")),
            company_size=parse_optional_str(row.get("company_size", "")),
            revenue_krw=parse_optional_int(row.get("revenue_krw", "")),
            website=parse_optional_str(row.get("website", "")),
            owner=parse_optional_str(row.get("owner", "")),
            lead_status=parse_optional_str(row.get("lead_status", "")),
            lifecycle_stage=parse_optional_str(row.get("lifecycle_stage", "")),
            score=parse_optional_int(row.get("score", "")),
            utm_source=parse_optional_str(row.get("utm_source", "")),
            utm_medium=parse_optional_str(row.get("utm_medium", "")),
            utm_campaign=parse_optional_str(row.get("utm_campaign", "")),
            last_activity_date=parse_optional_str(row.get("last_activity_date", "")),
            amount_krw=parse_optional_int(row.get("amount_krw", "")),
            created_date=parse_optional_str(row.get("created_date", "")),
            consent_status=parse_optional_str(row.get("consent_status", "")),
            expected_dynamic_match=parse_bool(row.get("expected_dynamic_match", "")),
            notes=parse_optional_str(row.get("notes", "")),
            automation_enabled=parse_bool_with_default(row.get("automation_enabled", ""), True),
            priority=parse_optional_str(row.get("priority", "")),
            expected_create_success=parse_bool_with_default(
                row.get("expected_create_success", ""),
                True,
            ),
            expected_fail_reason=parse_optional_str(row.get("expected_fail_reason", "")),
            title_override=parse_raw_str(row.get("title_override", "")),
            title_should_be_valid=parse_bool_with_default(
                row.get("title_should_be_valid", ""),
                True,
            ),
            company_select_text=parse_optional_str(row.get("company_select_text", "")),
            contact_select_text=parse_optional_str(row.get("contact_select_text", "")),
        )


@dataclass(frozen=True)
class LeadFormVariables:
    case_id: str
    lead_title: str
    contact_full_name: str
    contact_email: str
    contact_phone: Optional[str]
    contact_mobile: Optional[str]
    company_name: Optional[str]
    contact_job_title: Optional[str]
    contact_department: Optional[str]
    country: Optional[str]
    city: Optional[str]
    industry: Optional[str]
    company_size: Optional[str]
    company_revenue_krw: Optional[int]
    company_website: Optional[str]
    owner: Optional[str]
    lead_status: Optional[str]
    lifecycle_stage: Optional[str]
    score: Optional[int]
    utm_source: Optional[str]
    utm_medium: Optional[str]
    utm_campaign: Optional[str]
    last_activity_date: Optional[str]
    amount_krw: Optional[int]
    created_date: Optional[str]
    consent_status: Optional[str]
    expected_dynamic_match: bool
    notes: Optional[str]
    automation_enabled: bool
    priority: Optional[str]
    expected_create_success: bool
    expected_fail_reason: Optional[str]
    title_override: str
    title_should_be_valid: bool
    company_select_text: Optional[str]
    contact_select_text: Optional[str]


def build_form_variables(record: LeadSeedRecord) -> LeadFormVariables:
    return LeadFormVariables(
        case_id=record.case_id,
        lead_title=record.title,
        contact_full_name=record.full_name,
        contact_email=record.email,
        contact_phone=record.phone,
        contact_mobile=record.mobile,
        company_name=record.company_name,
        contact_job_title=record.job_title,
        contact_department=record.department,
        country=record.country,
        city=record.city,
        industry=record.industry,
        company_size=record.company_size,
        company_revenue_krw=record.revenue_krw,
        company_website=record.website,
        owner=record.owner,
        lead_status=record.lead_status,
        lifecycle_stage=record.lifecycle_stage,
        score=record.score,
        utm_source=record.utm_source,
        utm_medium=record.utm_medium,
        utm_campaign=record.utm_campaign,
        last_activity_date=record.last_activity_date,
        amount_krw=record.amount_krw,
        created_date=record.created_date,
        consent_status=record.consent_status,
        expected_dynamic_match=record.expected_dynamic_match,
        notes=record.notes,
        automation_enabled=record.automation_enabled,
        priority=record.priority,
        expected_create_success=record.expected_create_success,
        expected_fail_reason=record.expected_fail_reason,
        title_override=record.title_override,
        title_should_be_valid=record.title_should_be_valid,
        company_select_text=record.company_select_text,
        contact_select_text=record.contact_select_text,
    )


def load_lead_seed_records(csv_path: Path) -> list[LeadSeedRecord]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [LeadSeedRecord.from_csv_row(row) for row in reader]


def select_records(records: list[LeadSeedRecord], case_id: Optional[str]) -> list[LeadSeedRecord]:
    if not case_id:
        return [record for record in records if record.automation_enabled]

    selected = [record for record in records if record.case_id == case_id]
    if not selected:
        raise ValueError(f"case_id not found: {case_id}")
    return selected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load lead_seed.csv and map rows into automation variables.",
    )
    parser.add_argument(
        "--csv",
        default="data/lead_seed.csv",
        help="Path to lead seed CSV file.",
    )
    parser.add_argument(
        "--case-id",
        default=None,
        help="Optional case_id filter.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Max number of mapped variable objects to print.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    script_dir = Path(__file__).resolve().parent
    csv_path = (script_dir / args.csv).resolve() if not Path(args.csv).is_absolute() else Path(args.csv)

    records = load_lead_seed_records(csv_path)
    selected = select_records(records, args.case_id)
    mapped = [build_form_variables(record) for record in selected]

    print(f"Loaded records: {len(records)}")
    print(f"Selected records: {len(selected)}")

    for index, variables in enumerate(mapped[: args.limit], start=1):
        print(f"\n--- Variables #{index} (case_id={variables.case_id}) ---")
        for key, value in asdict(variables).items():
            print(f"{key}={value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
