import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Path, status
from httpx import Response

# app
app: FastAPI = FastAPI()

data = {"index": -1, "value": "hello fast api!"}


@app.get(path="/api/v1/data/{number}", status_code=status.HTTP_200_OK)
def get_data(
    number: int = Path(title="The data to get (based on number)", ge=1, le=15)
) -> list:
    result = []
    for x in range(number):
        result.append({"index": x, "value": "hello fast api!"})
    return result


@app.get(path="/api/v1/pokemon/{number}", status_code=status.HTTP_200_OK)
def get_pokemon(
    number: int = Path(title="The Pokémon to get (based on number)", ge=1, le=151)
) -> dict:
    pokemon_url: str = f"https://pokeapi.co/api/v2/pokemon/{number}"

    try:
        response: Response = httpx.get(url=pokemon_url)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not send a request to {pokemon_url}, {e}",
        )

    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=9090, reload=True)
