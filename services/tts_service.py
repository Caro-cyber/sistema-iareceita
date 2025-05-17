# services/tts_service.py
from google.cloud import texttospeech
import os

client_tts = None

def init_tts_client():
    global client_tts
    if client_tts is None:
        try:
            if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
                print("Atenção: GOOGLE_APPLICATION_CREDENTIALS não está definida.")
                print("O TTS pode não funcionar sem autenticação adequada.")
            client_tts = texttospeech.TextToSpeechClient()
            print("Cliente Google Text-to-Speech inicializado.")
            # Lista as vozes disponíveis em português
            list_available_voices("pt-BR")
        except Exception as e:
            print(f"Erro ao inicializar o cliente TTS: {e}")
            client_tts = None
    return client_tts

def list_available_voices(language_code="pt-BR"):
    """Lista todas as vozes disponíveis para o idioma especificado."""
    if not client_tts:
        print("Cliente TTS não inicializado.")
        return None
    
    try:
        # Lista todas as vozes disponíveis
        response = client_tts.list_voices(language_code=language_code)
        print(f"\nVozes disponíveis em {language_code}:")
        for voice in response.voices:
            # Mostra detalhes de cada voz
            print(f"Nome: {voice.name}")
            print(f"Gênero: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
            print(f"Taxa de amostragem: {voice.natural_sample_rate_hertz}Hz")
            print("Idiomas suportados:", [language.name for language in voice.language_codes])
            print("-" * 50)
        return response.voices
    except Exception as e:
        print(f"Erro ao listar vozes: {e}")
        return None

def generate_audio_instructions(text_instructions, output_filename_no_ext, lang_code="pt-BR"):
    """
    Converte o texto das instruções em um arquivo de áudio MP3.
    Retorna o caminho para o arquivo de áudio gerado ou None em caso de erro.
    """
    if not client_tts:
        print("Cliente TTS não inicializado.")
        return None

    synthesis_input = texttospeech.SynthesisInput(text=text_instructions)

    # Configuração da voz - usando uma voz específica do Brasil
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code,
        name="pt-BR-Standard-B", # Voz neural masculina
        # Outras opções de vozes:
        # "pt-BR-Neural2-A" - Voz neural feminina
        # "pt-BR-Neural2-C" - Voz neural feminina
        # "pt-BR-Standard-A" - Voz padrão feminina
        # "pt-BR-Standard-B" - Voz padrão masculina
        # "pt-BR-Standard-C" - Voz padrão feminina
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Configuração do áudio com ajustes de velocidade e tom
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.9,  # Velocidade um pouco mais lenta (1.0 é normal)
        pitch=0,           # Tom normal (pode ser ajustado de -20.0 a +20.0)
    )

    try:
        response = client_tts.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Garantir que o diretório existe
        audio_dir = os.path.join("static", "audio")
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        # Usar os.path.join para criar o caminho do arquivo corretamente
        output_filepath = os.path.join(audio_dir, f"{output_filename_no_ext}.mp3")

        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
            print(f'Áudio gerado e salvo em "{output_filepath}"')
        
        # Retornar o caminho relativo usando barras normais (/) em vez de barras invertidas (\)
        return f"audio/{output_filename_no_ext}.mp3"

    except Exception as e:
        print(f"Erro ao gerar áudio: {e}")
        return None 