import pytest
from em_parser import Parser


class TestCampaignTypes:

    @pytest.mark.parametrize(
        'campaign_name,airline_code,campaign_type',
        [(r'GS:en-US_CO=SteamshipAuthority/Geo@US', '9K', 'Competitor')]
    )
    def test_competitor(self, campaign_name, airline_code, campaign_type):
        result = Parser(cached=False).parse(campaign_name, airline_code=airline_code)
        assert result['CampaignType'] == campaign_type
