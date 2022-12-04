import os
import json
from enum import Enum
from fastapi import FastAPI
from fastapi.responses import FileResponse
from openbb_terminal.economy.econdb_view import  show_treasuries
from openbb_terminal.economy.wsj_model import us_indices, market_overview

class OutputFormat(str, Enum):
    text = "text"
    json = "json"

app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/bigger-applications/
@app.get("/treasury_chart")
async def get_spreadsheet(start_date: str, end_date: str):
    """
        Returns us treasury chart
    """
    temp_filename = "treasury.png"
    if start_date and end_date:
        show_treasuries(maturities=["3m", "1y", "3y", "5y", "10y", "20y", "30y" ], start_date=start_date, end_date=end_date, export=temp_filename)
    else:
        show_treasuries(maturities=["3m", "1y", "3y", "5y", "10y", "20y", "30y" ], export=temp_filename)
    # return image temp.png
    stream = os.popen('cd ~ && pwd')
    root_dir = stream.read()
    # /home/codespace/OpenBBUserData/exports/temp.png
    # find root directory/OpenBBUserData/exports
    sample_dir = root_dir.strip()
    # root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    temp_image = os.path.join(sample_dir, "OpenBBUserData", "exports", temp_filename)
    return FileResponse(temp_image)


@app.get("/market_overview")
async def get_market_overview(fmt: OutputFormat = OutputFormat.text):
    """
    Returns market overview
    """
    pd = market_overview()
    pd.columns.values[0] = "name"
    # dataframe to csv for buffer
    if fmt == OutputFormat.text:
        return pd.to_csv(index=False)
    elif fmt == OutputFormat.json:
        return json.loads(pd.to_json(orient="split"))
    return pd

@app.get("/us_indices")
async def get_us_indices(fmt: OutputFormat = OutputFormat.text):
    """
    Returns us indices
    """
    pd = us_indices()
    # set index name to index
    # pd.index.name = "index"
    pd.columns.values[0] = "index"
    if fmt == OutputFormat.text:
        return pd.to_csv(index=False)
    elif fmt == OutputFormat.json:
        return json.loads(pd.to_json(orient="split"))
    return pd