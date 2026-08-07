#!/usr/bin/env python3
"""
Résumé generator for Lohit P.

Generates two ATS-friendly, single-column PDFs using reportlab:
  - Lohit_P_Software_Engineer.pdf      (primary; what the portfolio links)
  - Lohit_P_React_Native_Product_Engineer.pdf

Positioning: a complete software engineer with deep mobile roots — not
"a React Native developer." RN is a strength, not the identity.

No fabricated metrics. Real achievements surfaced at senior altitude:
  - Background-location native module (survives process termination)
  - Real-time systems + Convex -> self-hosted Socket.IO cost migration
  - Testing infrastructure (unit/integration/E2E + seed data)
  - OTA + end-to-end CI/CD ownership
  - Lean-team leadership (1 yr)

Usage:
  python3 generate_resumes.py            # writes both PDFs to ../assets/
  python3 generate_resumes.py --preview  # opens them after generating
"""

import os
import subprocess
import sys

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    HRFlowable, KeepTogether,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))

# ---------------------------------------------------------------------------
# Contact (single source of truth)
# ---------------------------------------------------------------------------
NAME = "LOHIT P"
EMAIL = "lohitcode@gmail.com"
LOCATION = "Hyderabad, India"
PHONE = "+91 8629924736"
SITE = "lohitcode.com"
GITHUB = "github.com/lohitcode"

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
# reportlab ships with Helvetica (clean, ATS-safe, universally available).
INK = HexColor("#1a1a1a")
MUTED = HexColor("#555555")
RULE = HexColor("#c8c8c8")
ACCENT = HexColor("#3a3a3a")

BODY = "Helvetica"
BODY_B = "Helvetica-Bold"
BODY_I = "Helvetica-Oblique"


def styles():
    s = {}
    s["name"] = ParagraphStyle(
        "name", fontName=BODY_B, fontSize=20, leading=24,
        textColor=INK, alignment=TA_LEFT, spaceAfter=2,
    )
    s["title"] = ParagraphStyle(
        "title", fontName=BODY, fontSize=9.5, leading=13,
        textColor=MUTED, alignment=TA_LEFT, spaceAfter=4,
    )
    s["contact"] = ParagraphStyle(
        "contact", fontName=BODY, fontSize=8.5, leading=12,
        textColor=MUTED, alignment=TA_LEFT, spaceAfter=2,
    )
    s["section"] = ParagraphStyle(
        "section", fontName=BODY_B, fontSize=9.5, leading=12,
        textColor=INK, alignment=TA_LEFT,
        spaceBefore=10, spaceAfter=4,
    )
    s["role"] = ParagraphStyle(
        "role", fontName=BODY_B, fontSize=9.5, leading=12,
        textColor=INK, alignment=TA_LEFT, spaceBefore=6, spaceAfter=0,
    )
    s["company"] = ParagraphStyle(
        "company", fontName=BODY_I, fontSize=9, leading=11,
        textColor=MUTED, alignment=TA_LEFT, spaceAfter=3,
    )
    s["body"] = ParagraphStyle(
        "body", fontName=BODY, fontSize=9, leading=12.5,
        textColor=INK, alignment=TA_LEFT, spaceAfter=2,
    )
    s["bullet"] = ParagraphStyle(
        "bullet", fontName=BODY, fontSize=9, leading=12.5,
        textColor=INK, alignment=TA_LEFT,
        leftIndent=12, firstLineIndent=-8, spaceAfter=2.5, bulletIndent=0,
    )
    s["skills"] = ParagraphStyle(
        "skills", fontName=BODY, fontSize=8.8, leading=12,
        textColor=INK, alignment=TA_LEFT, spaceAfter=2.5,
    )
    return s


S = styles()


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=RULE,
                      spaceBefore=2, spaceAfter=2)


def section(title):
    return [Spacer(1, 4), Paragraph(title.upper(), S["section"]), hr()]


def bullets(items):
    return [Paragraph(f"\u2022&nbsp;&nbsp;{t}", S["bullet"]) for t in items]


def role_block(title, company, date, *items, published=None):
    """A role header + bullets, kept together so it doesn't split awkwardly."""
    # date on the right of the role line via a simple inline approach
    head = Paragraph(f"{title}", S["role"])
    sub = Paragraph(f"{company} &nbsp;&nbsp;|&nbsp;&nbsp; {date}", S["company"])
    flow = [head, sub]
    flow += bullets(items)
    if published:
        flow.append(Paragraph(f"<i>{published}</i>", S["body"]))
    return KeepTogether(flow)


# ---------------------------------------------------------------------------
# Shared content (the real achievements, senior altitude)
# ---------------------------------------------------------------------------

TURTIL_ACHIEVEMENTS = [
    (
        "Led mobile delivery within a lean team for the past year — owning React "
        "Native/Expo releases end to end, supporting developers, reviewing "
        "implementation choices and influencing what we built next."
    ),
    (
        "Owned the complete iOS and Android release lifecycle: OTA updates via "
        "EAS, end-to-end CI/CD, App Store and Play Store submissions, compliance, "
        "review responses and production rollouts."
    ),
    (
        "Built a native module to keep location collection alive after the React "
        "Native process was terminated, buffering locally and syncing to the "
        "server on reconnect — behavior the JS runtime cannot provide on its own."
    ),
    (
        "Designed real-time chat and live poll updates over WebSockets; migrated "
        "from a managed platform (Convex) to a self-hosted Socket.IO service to "
        "control cost as usage grew."
    ),
    (
        "Built testing infrastructure across unit, integration and end-to-end "
        "(Maestro) layers, backed by reliable backend seed data so releases could "
        "be validated automatically across iOS and Android."
    ),
    (
        "Implemented offline-first features (e.g. timetable access via local "
        "SQLite) so core functionality stayed available on poor or absent "
        "networks, with tuned scroll and data fetching for low-end devices."
    ),
]

TURTIL_PLATFORM = [
    (
        "Built full-stack features using TypeScript, React/Next.js, Hono, "
        "PostgreSQL, Drizzle and Zod, including authentication, payments, "
        "analytics and real-time workflows."
    ),
    (
        "Engineered CI/CD with change detection, parallel validation, Playwright "
        "testing and coverage gates; used AI for planning and implementation "
        "while independently validating correctness before production."
    ),
    (
        "Operated AWS infrastructure with Terraform, ECS, EC2, RDS, Lambda, S3 "
        "and CloudFront, supported by OpenTelemetry, Grafana, Prometheus, Loki "
        "and alerting."
    ),
    (
        "Built Go services for Redis-backed background jobs and runner "
        "orchestration with retries, deduplication, scheduling and operational "
        "metrics."
    ),
]

HYPOSOFT_ACHIEVEMENTS = [
    (
        "Built and shipped React Native products for cold-storage commerce and "
        "sports communities, including booking, inventory, social and real-time "
        "notification workflows."
    ),
    (
        "Implemented Node.js and MongoDB backends, Socket.IO real-time features, "
        "Firebase Cloud Messaging and payment flows using Razorpay, PhonePe and "
        "Paytm."
    ),
    (
        "Delivered polished, responsive mobile experiences and collaborated "
        "closely on evolving product requirements and design."
    ),
]

INTERN_ACHIEVEMENTS = [
    (
        "Built two published React Native applications — FarmOR Partner (1K+ "
        "Google Play downloads) and FarmOR Kisaan — covering B2B purchasing, "
        "orders and inventory; also delivered FarmOR's responsive marketing "
        "website."
    ),
]

INDEPENDENT_ACHIEVEMENTS = [
    (
        "Deepening computer-science fundamentals through an implementation-first "
        "curriculum covering Go, PostgreSQL/SQL, data structures and algorithms, "
        "networking, operating systems, security, deployment and system design."
    ),
    (
        "Building production-shaped Go HTTP services with pgx, migrations and "
        "SQLC while documenting each concept and defending implementation "
        "decisions independently."
    ),
]


# ---------------------------------------------------------------------------
# Document scaffolding
# ---------------------------------------------------------------------------

def build(path, role_title, profile, extra_sections, footer_tag):
    """extra_sections is a list of flowable lists already built by the caller."""
    doc = BaseDocTemplate(
        path, pagesize=LETTER,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.55 * inch, bottomMargin=0.5 * inch,
        title=f"Lohit P - {footer_tag}", author="Lohit P",
    )
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height, id="main",
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="t", frames=[frame])])

    story = []
    # Header
    story.append(Paragraph(NAME, S["name"]))
    story.append(Paragraph(role_title, S["title"]))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        f"{LOCATION} &nbsp;|&nbsp; {PHONE} &nbsp;|&nbsp; {EMAIL} &nbsp;|&nbsp; "
        f"{SITE} &nbsp;|&nbsp; {GITHUB}",
        S["contact"],
    ))
    story.append(hr())

    # Profile
    story += section("Profile")
    story.append(Paragraph(profile, S["body"]))

    # Caller-provided sections
    for sec in extra_sections:
        story += sec

    doc.build(story)
    return path


# ---------------------------------------------------------------------------
# Software Engineer résumé
# ---------------------------------------------------------------------------

def build_software_engineer():
    profile = (
        "Software engineer with 4+ years building production products end to end "
        "&mdash; the mobile app, the APIs and data behind it, and the "
        "infrastructure it runs on. Started in React Native and it remains a "
        "deepest strength, but the work spans real-time systems, background "
        "services, testing infrastructure, cost-driven architecture decisions and "
        "production operations. Led mobile delivery within a lean team for the "
        "past year, owning releases and influencing what was built next. Uses "
        "AI-assisted workflows to accelerate delivery while retaining "
        "responsibility for architecture, review and correctness."
    )

    rn_expertise = section("React Native depth") + [
        Paragraph(
            "<b>Release ownership:</b> EAS Build/Submit/Update, OTA updates, App "
            "Store and Play Store compliance, review responses and production "
            "releases across iOS and Android.", S["skills"]),
        Paragraph(
            "<b>Delivery systems:</b> end-to-end mobile CI/CD, "
            "environment-aware builds, release channels, crash monitoring and "
            "rollout validation.", S["skills"]),
        Paragraph(
            "<b>Quality &amp; testing:</b> unit, integration and end-to-end "
            "(Maestro) testing backed by reliable backend seed data, failure-path "
            "validation and production analytics.", S["skills"]),
        Paragraph(
            "<b>Systems work:</b> native modules bridging platform behavior the JS "
            "runtime cannot provide, offline-first persistence, real-time "
            "communication and push/deep-link integration.", S["skills"]),
        Paragraph(
            "<b>Leadership:</b> led mobile delivery within a lean team, supported "
            "developers, reviewed implementation choices and worked closely with "
            "designers on product assets and store requirements.", S["skills"]),
    ]

    experience = section("Experience") + [
        role_block(
            "Full-Stack &amp; Infrastructure Engineer", "Turtil, Hyderabad",
            "Mar 2024 &ndash; May 2026",
            *TURTIL_ACHIEVEMENTS,
            published="Published apps: Parentz (10K+ downloads) | Turtil Campus (1K+)",
        ),
        Spacer(1, 3),
        Paragraph("Broader product &amp; platform work", S["body"]),
        *bullets(TURTIL_PLATFORM),
        Spacer(1, 4),
        role_block(
            "Mobile, Backend &amp; Frontend Engineer",
            "Hyposoft Global Solutions, Hyderabad", "Feb 2022 &ndash; Dec 2023",
            *HYPOSOFT_ACHIEVEMENTS,
        ),
        Spacer(1, 4),
        role_block(
            "Frontend &amp; Mobile Application Engineer (Intern)",
            "Hyposoft Global Solutions, Hyderabad", "Dec 2021 &ndash; Jan 2022",
            *INTERN_ACHIEVEMENTS,
        ),
    ]

    independent = section("Independent study &amp; product development") + [
        role_block(
            "Independent Study &amp; Builder", "Self-directed, Hyderabad",
            "May 2026 &ndash; Present",
            *INDEPENDENT_ACHIEVEMENTS,
        ),
        Paragraph(f"<i>{GITHUB}/computer-science-from-scratch</i>", S["body"]),
    ]

    foundation = section("Technical foundation") + [
        Paragraph("<b>Languages:</b> TypeScript, JavaScript, Go, SQL", S["skills"]),
        Paragraph(
            "<b>Backend &amp; data:</b> Node.js, Hono, Express, PostgreSQL, Drizzle, "
            "Redis/Valkey, Asynq, REST, Socket.IO", S["skills"]),
        Paragraph(
            "<b>Cloud &amp; operations:</b> AWS, Terraform, Docker, GitHub Actions, "
            "OpenTelemetry, Grafana, Sentry, PostHog", S["skills"]),
        Paragraph(
            "<b>Web:</b> React, Next.js, Tailwind CSS, TanStack Query, Zustand, "
            "React Hook Form", S["skills"]),
        Paragraph(
            "<b>Foundations:</b> data structures and algorithms, relational "
            "databases, concurrency, networking and operating-system fundamentals",
            S["skills"]),
    ]

    education = section("Education") + [
        Paragraph(
            "<b>Bachelor of Technology (B.Tech.)</b> &nbsp;|&nbsp; 2017 &ndash; 2021",
            S["body"]),
        Paragraph(
            "Malla Reddy Institute of Technology &amp; Science, Hyderabad",
            S["body"]),
    ]

    out = os.path.join(ASSETS, "Lohit_P_Software_Engineer.pdf")
    return build(
        out,
        "Software Engineer | Mobile, Full-Stack &amp; Platform Engineering",
        profile,
        [rn_expertise, experience, independent, foundation, education],
        "Software Engineer",
    )


# ---------------------------------------------------------------------------
# React Native Product Engineer résumé
# ---------------------------------------------------------------------------

def build_rn_product_engineer():
    profile = (
        "Product engineer with 4+ years shipping production software end to end. "
        "Owns the complete lifecycle &mdash; product decisions, architecture, "
        "implementation, testing, store release, observability and iteration &mdash; "
        "with React Native/Expo as a deepest strength and full-stack depth across "
        "TypeScript, Node.js, Next.js, PostgreSQL and AWS. Led mobile delivery "
        "within a lean team for the past year, owning releases and influencing "
        "what was built next. Uses AI-assisted workflows daily to accelerate "
        "delivery while retaining responsibility for system design, code review, "
        "testing, security and production outcomes."
    )

    core_skills = section("Core skills") + [
        Paragraph(
            "<b>Mobile:</b> React Native, Expo, Expo Router, EAS Build/Submit/"
            "Update, offline-first data, native module integration, push "
            "notifications, deep links, App Store Connect, Google Play Console, "
            "Maestro", S["skills"]),
        Paragraph(
            "<b>Frontend:</b> TypeScript, JavaScript, React, Next.js, Tailwind "
            "CSS, TanStack Query, Zustand", S["skills"]),
        Paragraph(
            "<b>Backend &amp; data:</b> Node.js, Hono, Express, Go, PostgreSQL, "
            "SQL, Drizzle ORM, Redis/Valkey, Asynq, Socket.IO, REST APIs, "
            "transactions, indexing and data modeling", S["skills"]),
        Paragraph(
            "<b>Cloud &amp; delivery:</b> AWS (ECS, EC2, Lambda, RDS, S3, "
            "CloudFront, SES, IAM), Terraform, Docker, GitHub Actions, SST, "
            "CI/CD", S["skills"]),
        Paragraph(
            "<b>Quality &amp; operations:</b> Playwright, Vitest, Jest, Maestro, "
            "OpenTelemetry, Grafana, Prometheus, Loki, Sentry, PostHog",
            S["skills"]),
        Paragraph(
            "<b>Foundations:</b> data structures and algorithms, relational "
            "databases, concurrency, networking and operating-system fundamentals",
            S["skills"]),
    ]

    # RN version uses slightly longer narrative bullets (its original style)
    turtil = [
        (
            "Owned React Native/Expo delivery for Parentz (formerly Turtil "
            "Student; 10K+ downloads) and Turtil Campus (1K+), reaching 11K+ "
            "combined Google Play downloads, and led mobile delivery within a "
            "lean team &mdash; supporting developers, reviewing implementation "
            "choices and influencing what we built next."
        ),
        (
            "Owned the complete iOS and Android release lifecycle: OTA updates "
            "via EAS, end-to-end CI/CD, App Store and Play Store submissions, "
            "review responses, compliance and production releases."
        ),
        (
            "Built a native module to keep location collection alive after the "
            "React Native process was terminated, buffering locally and syncing "
            "to the server on reconnect."
        ),
        (
            "Designed real-time chat and live poll updates over WebSockets; "
            "migrated from a managed platform (Convex) to a self-hosted "
            "Socket.IO service to control cost as usage grew."
        ),
        (
            "Built testing infrastructure across unit, integration and "
            "end-to-end (Maestro) layers, backed by reliable backend seed data "
            "so releases could be validated automatically."
        ),
        (
            "Implemented offline timetable access with local SQLite persistence "
            "so students and staff could view schedules during unreliable or "
            "unavailable network conditions, with considered loading, empty and "
            "error states."
        ),
        (
            "Built full-stack features for a multi-tenant campus-management "
            "platform using TypeScript, React/Next.js, Hono, PostgreSQL, Drizzle "
            "and Zod; contributed to relational schema design, "
            "institution-scoped access controls and workflows spanning "
            "academics, finance, HR, library, inventory and learning."
        ),
        (
            "Engineered CI/CD with change detection, parallel lint, type-check, "
            "build and test stages, Playwright E2E testing and diff-coverage "
            "gates; used AI for planning, implementation and review while "
            "independently validating correctness and production behavior."
        ),
        (
            "Reduced development-environment infrastructure cost by moving "
            "suitable ECS workloads from per-task Fargate capacity to fixed "
            "EC2-backed capacity, while retaining autoscaling ECS services for "
            "staging and production workloads."
        ),
        (
            "Operated AWS infrastructure across dev, staging, demo and "
            "production with Terraform, ECS, RDS, Lambda, S3 and CloudFront; "
            "established OpenTelemetry, Grafana, Prometheus, Loki and alerting "
            "for production visibility."
        ),
        (
            "Built Go services for Redis-backed background jobs and runner "
            "orchestration, including retries with exponential backoff, "
            "deduplication, scheduled execution, ephemeral EC2 workers and "
            "custom operational metrics."
        ),
    ]

    experience = section("Experience") + [
        role_block(
            "Full-Stack &amp; Infrastructure Engineer", "Turtil, Hyderabad",
            "Mar 2024 &ndash; May 2026",
            *turtil,
        ),
        Spacer(1, 4),
        role_block(
            "Mobile Application &amp; Backend Engineer",
            "Hyposoft Global Solutions, Hyderabad", "Feb 2022 &ndash; Dec 2023",
            *HYPOSOFT_ACHIEVEMENTS,
        ),
        Spacer(1, 4),
        role_block(
            "Frontend &amp; Mobile Application Engineer (Intern)",
            "Hyposoft Global Solutions, Hyderabad", "Dec 2021 &ndash; Jan 2022",
            *INTERN_ACHIEVEMENTS,
        ),
    ]

    independent = section("Independent engineering &amp; product development") + [
        role_block(
            "Independent Study &amp; Builder", "Self-directed, Hyderabad",
            "May 2026 &ndash; Present",
            *INDEPENDENT_ACHIEVEMENTS,
        ),
        Paragraph(f"<i>{GITHUB}/computer-science-from-scratch</i>", S["body"]),
    ]

    highlights = section("Selected engineering highlights") + [
        Paragraph(
            "<b>Agentic product experience:</b> Gemini assistant with autonomous "
            "tool use, SSE streaming, page context, prompt-injection hardening "
            "and PostHog LLM analytics.", S["skills"]),
        Paragraph(
            "<b>Production integrations:</b> Razorpay, PhonePe, Cashfree, Twilio, "
            "Firebase, FFmpeg transcoding, S3/CloudFront delivery and "
            "WebSocket-based authentication.", S["skills"]),
        Paragraph(
            "<b>Operational ownership:</b> four AWS environments, reusable "
            "Terraform modules, deployment automation, autoscaling services, "
            "observability dashboards and incident alerts.", S["skills"]),
    ]

    education = section("Education") + [
        Paragraph(
            "<b>Bachelor of Technology (B.Tech.)</b> &nbsp;|&nbsp; 2017 &ndash; 2021",
            S["body"]),
        Paragraph(
            "Malla Reddy Institute of Technology &amp; Science, Hyderabad",
            S["body"]),
    ]

    out = os.path.join(ASSETS, "Lohit_P_React_Native_Product_Engineer.pdf")
    return build(
        out,
        "React Native Product Engineer | Full-Stack &amp; Platform Engineer",
        profile,
        [core_skills, experience, independent, highlights, education],
        "React Native Product Engineer",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(ASSETS, exist_ok=True)
    se = build_software_engineer()
    rn = build_rn_product_engineer()
    print(f"wrote {se}")
    print(f"wrote {rn}")

    if "--preview" in sys.argv:
        for p in (se, rn):
            subprocess.run(["open", p])


if __name__ == "__main__":
    main()
