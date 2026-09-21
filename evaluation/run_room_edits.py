"""Run the four-image, single-variant room-edit smoke evaluation."""

import argparse
import base64
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "/app")
import app


CASES = [
    ("118.jpg", "Restore only the unfinished wall surfaces with warm ivory limewash; preserve the ornate historic ceiling, windows, radiator, floor, architecture, and camera view exactly."),
    ("131.jpg", "Renovate the bedroom finishes: replace the damaged wall finish with warm white plaster and the damaged floor surface with natural light oak; preserve the room geometry, window, radiator, furniture positions, and camera view exactly."),
    ("144.jpg", "Replace only the damaged floor with realistic medium-tone reclaimed oak flooring; preserve every wall, window, ceiling, object, room dimension, lighting condition, and the camera view exactly."),
    ("356.jpg", "Restore only the damaged wall surfaces with soft warm-white plaster; preserve the wood floor, fireplace, sofa, cabinet, window, ceiling, architecture, lighting, and camera view exactly."),
]


def data_url(path: Path) -> str:
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else f"image/{path.suffix[1:].lower()}"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--case", choices=[Path(item[0]).stem for item in CASES])
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    selected_cases = [item for item in CASES if not args.case or Path(item[0]).stem == args.case]
    report = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "model": app.OPENAI_IMAGE_MODELS["high_quality"],
        "planned_generation_calls": len(selected_cases),
        "estimated_cost_usd": round(len(selected_cases) * app.ESTIMATED_COST_MICROS["high_quality"] / 1_000_000, 2),
        "cases": [],
    }

    for filename, instruction in selected_cases:
        record = {"source": filename, "instruction": instruction, "status": "failed"}
        try:
            source = app.validate_image_data(data_url(args.input_dir / filename))
            app.moderate_input(instruction, source)
            prompt = app.build_visualization_prompt(instruction, True)
            results = app.run_openai_image_edit(
                source, prompt, app.OPENAI_IMAGE_MODELS["high_quality"], 1
            )
            accepted, rejected, scores = app.filter_similar_room_outputs(source, results)
            record.update({"similarity_score": scores[0] if scores else None, "rejected_for_drift": rejected})
            if not accepted:
                record["error"] = "scene_drift"
            else:
                app.moderate_output("", accepted)
                output_name = f"{Path(filename).stem}_edited.png"
                (args.output_dir / output_name).write_bytes(base64.b64decode(accepted[0]))
                record.update({"status": "completed", "output": output_name})
        except Exception as exc:
            record["error"] = type(exc).__name__
            record["provider_diagnostic"] = {
                "status_code": getattr(exc, "status_code", None),
                "code": getattr(exc, "code", None),
                "param": getattr(exc, "param", None),
                "message": str(exc)[:500],
            }
        report["cases"].append(record)
        (args.output_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    report["completed_at"] = datetime.now(timezone.utc).isoformat()
    (args.output_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if all(case["status"] == "completed" for case in report["cases"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
