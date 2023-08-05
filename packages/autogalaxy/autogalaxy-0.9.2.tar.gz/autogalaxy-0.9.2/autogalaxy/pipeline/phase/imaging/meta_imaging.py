from autogalaxy.dataset import imaging
from autogalaxy.pipeline.phase.dataset import meta_dataset


class MetaImaging(meta_dataset.MetaDataset):
    def __init__(
        self,
        model,
        sub_size=2,
        is_hyper_phase=False,
        signal_to_noise_limit=None,
        inversion_pixel_limit=None,
        psf_shape_2d=None,
        bin_up_factor=None,
    ):

        super().__init__(
            model=model,
            sub_size=sub_size,
            is_hyper_phase=is_hyper_phase,
            signal_to_noise_limit=signal_to_noise_limit,
            inversion_pixel_limit=inversion_pixel_limit,
        )
        self.psf_shape_2d = psf_shape_2d
        self.bin_up_factor = bin_up_factor

    def masked_dataset_from(self, dataset, mask, results):

        mask = self.mask_with_phase_sub_size_from_mask(mask=mask)

        if self.bin_up_factor is not None:

            dataset = dataset.binned_from_bin_up_factor(
                bin_up_factor=self.bin_up_factor
            )

            mask = mask.mapping.binned_mask_from_bin_up_factor(
                bin_up_factor=self.bin_up_factor
            )

        if self.signal_to_noise_limit is not None:
            dataset = dataset.signal_to_noise_limited_from_signal_to_noise_limit(
                signal_to_noise_limit=self.signal_to_noise_limit
            )

        masked_imaging = imaging.MaskedImaging(
            imaging=dataset,
            mask=mask,
            psf_shape_2d=self.psf_shape_2d,
            inversion_pixel_limit=self.inversion_pixel_limit,
        )

        return masked_imaging
