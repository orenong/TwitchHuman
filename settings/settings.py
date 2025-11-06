from pydantic import BaseModel, Field
from typing import Literal
from consts import DEFAULT_PERSONALITY
import yaml
import os

class Settings(BaseModel):
    drunkenness: int = Field(ge=0,description="How often the bot will do mistakes or do weird stuff. Controls typos too. Anything above 100 is crazy")
    streamer_channel_name: str = Field(description="the stream where the bot will work")
    llm_model_name: str
    llm_provider: Literal["ollama", "openai", "lm-studio","gemini"]
    llm_key: str = Field(default="no-key")
    whisper_model_size: str = Field(default="small")
    hide_bboxes: list[tuple[int,int,int,int]] = Field(description="x1,y1,x2,y2 of bbox. The bot will be blind to what's inside these boxes. Useful when you want to hide the chat")
    personality: str = Field(default=DEFAULT_PERSONALITY)
    bot_username: str
    bot_twitch_key: str
    wpm: int


# Save to YAML
def save_settings(settings: Settings):
    filepath = os.getcwd() + "/settings/settings.yaml"
    with open(filepath, 'w') as f:
        # Convert Pydantic model to dict, then to YAML
        yaml.dump(settings.model_dump(), f, default_flow_style=False)

# Load from YAML
def load_settings() -> Settings:
    try:
        filepath = os.getcwd() + "/settings/settings.yaml"
        with open(filepath, 'r') as f:
            data = yaml.load(f,Loader=yaml.FullLoader)
            return Settings(**data)
    except Exception as e:
        print("The settings file is broken, fix it or reset your settings.{e}")


def reset_settings():
    settings = Settings(
        drunkenness=20,
        streamer_channel_name="orenog_live0",
        llm_model_name="qwen3-vl:4b-instruct-9500",
        llm_provider="ollama",
        hide_bboxes=[(0,0,0,0)],
        bot_username="bot",
        bot_twitch_key="166166166",
        wpm = "100"
    )
    save_settings(settings)
    print(load_settings())


settings = load_settings()
