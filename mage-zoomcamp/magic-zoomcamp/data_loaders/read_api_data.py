import io
import os
import requests
from pandas import DataFrame
from dotenv import load_dotenv
import nasdaqdatalink
from io import BytesIO
from zipfile import ZipFile

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(**kwargs) -> DataFrame:
    """
    Template for loading data from API
    """

    # Add logging
    kwarg_logger = kwargs.get('logger')

    kwarg_logger.info('Test logger info')
    kwarg_logger.warning('Test logger warning')
    kwarg_logger.error('Test logger error')

    # Config API to your own Nasdaq QUANDL account
    nasdaqdatalink.ApiConfig.api_key = os.getenv('QUANDL_API')
    df = nasdaqdatalink.get_table('SHARADAR/TICKERS', paginate=False)

    print(df.isnull().sum())
    
    return df



@test
def test_output(df, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
