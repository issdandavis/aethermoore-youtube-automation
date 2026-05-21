from aether_youtube_automation.package import VideoPackage
from aether_youtube_automation.review import review_video_package


def test_review_good_package_scores_high():
    package = VideoPackage(
        title="How I Automate My YouTube Workflow Without Losing Control",
        description="A practical walkthrough of a local-first workflow for creators with review gates and manual approval.",
        tags=("youtube automation", "creator tools", "workflow"),
        script=" ".join(["safe automation"] * 50),
        privacy="unlisted",
    )

    report = review_video_package(package)

    assert report.score >= 90
    assert not [finding for finding in report.findings if finding.severity == "fail"]


def test_review_invalid_privacy_fails():
    package = VideoPackage(
        title="Tiny",
        description="",
        tags=(),
        privacy="auto-public-now",
    )

    report = review_video_package(package)

    assert report.score < 70
    assert any(finding.field == "privacy" and finding.severity == "fail" for finding in report.findings)

