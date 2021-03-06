from deep_signature.data_generation.dataset_generation import EquiaffineCurvatureTupletsDatasetGenerator
from common import settings

if __name__ == '__main__':
    EquiaffineCurvatureTupletsDatasetGenerator.generate_tuples(
        dir_path=settings.level_curves_equiaffine_curvature_tuplets_dir_path,
        curves_dir_path=settings.level_curves_dir_path_train,
        sections_density=0.6,
        negative_examples_count=2,
        supporting_points_count=6,
        max_offset=12,
        chunksize=10000)
