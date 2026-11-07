from pathlib import Path

import pycolmap


def reconstruct(frames_dir):
    db = Path(f"{frames_dir}_database") / "database.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    sparse_dir = Path(f"{frames_dir}_sparse")
    sparse_dir.mkdir(parents=True, exist_ok=True)

    pycolmap.extract_features(
        image_path=frames_dir,
        database_path=db
    )

    pycolmap.match_sequential(database_path=db)

    reconstructions = pycolmap.incremental_mapping(
        database_path=db,
        image_path=frames_dir,
        output_path=sparse_dir
    )

    if not reconstructions:
        raise RuntimeError("No sparse model recontructed.")

    for model_id, reconstruction in reconstructions.items():
        model_path = sparse_dir / str(model_id)
        reconstruction.write(model_path)
        print(model_id, reconstruction.summary())
