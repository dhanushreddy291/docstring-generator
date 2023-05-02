from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface


def download_model():
    """

    Downloads and loads a pre-trained FastSpeech2 model from Hugging Face Hub, and generates speech for a given input text using the loaded model.

    Returns:
        A tuple containing the generated speech waveform and its sampling rate.

    Example Usage:
        >>> waveform, sampling_rate = download_model()
        >>> text = "Hello, how are you?"
        >>> speech = generate_speech(waveform, sampling_rate, text)

    """
    models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
        "facebook/fastspeech2-en-ljspeech",
        arg_overrides={"vocoder": "hifigan", "fp16": False},
    )
    model = models[0]
    TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
    generator = task.build_generator([model], cfg)

    text = "This is a test run of the download.py script."

    sample = TTSHubInterface.get_model_input(task, text)
    wav, rate = TTSHubInterface.get_prediction(task, model, generator, sample)


if __name__ == "__main__":
    download_model()
