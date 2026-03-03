"""API client for fetching gold rate data."""
import requests
import json
import urllib3
from datetime import datetime
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.config import config
from src.logger import logger
import re

# Suppress SSL warnings if verification is disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GoldRateClient:
    """Client for fetching gold rates from metals.live API."""
    
    def __init__(self):
        """Initialize the API client."""
        self.api_url = config.METALS_API_URL
        self.timeout = config.API_TIMEOUT
        self.data_file = config.DATA_FILE
        self.session = self._create_session()
    
    @staticmethod
    def _create_session():
        """Create a session with retry strategy."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=2,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        # Mount adapter with retry strategy
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def fetch_current_rates(self) -> dict:
        """
        Fetch current gold rates from goldpriceindia.com.
        
        Returns:
            Dictionary with gold rate data (22K and 24K rates in INR per gram)
            
        Raises:
            requests.RequestException: If API call fails
        """
        try:
            logger.info(f"Fetching gold rates from {self.api_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Fetch the webpage
            response = self.session.get(
                self.api_url, 
                timeout=self.timeout,
                verify=False,
                headers=headers
            )
            response.raise_for_status()
            
            # Parse the HTML content
            html_content = response.text
            rates = self._parse_goldpriceindia(html_content)
            
            if rates:
                logger.info("Successfully fetched gold rates from goldpriceindia.com")
                return rates
            else:
                logger.warning("Could not parse rates from goldpriceindia.com")
                return self._get_mock_data()
                
        except requests.RequestException as e:
            logger.error(f"Failed to fetch gold rates: {str(e)}")
            logger.warning("Using mock data for demonstration purposes")
            return self._get_mock_data()
    
    @staticmethod
    def _get_mock_data() -> dict:
        """
        Return mock gold rate data for demonstration.
        Rates are per gram in INR (Updated for March 4, 2026).
        
        Returns:
            Mock gold rate data
        """
        return {
            'rate_22k': 14740.00,  # Mock rate per gram in INR (March 4, 2026)
            'rate_24k': 16080.00,  # Mock rate per gram in INR (March 4, 2026)
            'timestamp': datetime.now().isoformat(),
            'source': 'mock_data'
        }
    
    @staticmethod
    def _parse_goldpriceindia(html_content: str) -> dict:
        """
        Parse gold rates from goldpriceindia.com HTML content.
        Extracts 22K and 24K rates per gram.
        
        Args:
            html_content: HTML content from the website
        
        Returns:
            Dictionary with 22K and 24K rates per gram
        """
        try:
            # The website shows:
            # 24K: ₹16,080 - gold price per gram | ₹1,60,802 - gold price per 10 grams
            # 22K: ₹14,740 - gold price per gram | ₹1,47,402 - gold price per 10 grams
            
            # Extract 24K per gram rate
            # Pattern: "₹16,080 - gold price per gram"
            pattern_24k = r'₹([\d,]+)\s*-\s*gold\s+price\s+per\s+gram'
            
            rates_24k = re.findall(pattern_24k, html_content, re.IGNORECASE)
            rates_22k = []
            
            # Find all currency patterns and then match them with carat types
            all_currency_matches = list(re.finditer(r'(₹[\d,]+)\s*-\s*gold\s+(?:rate|price)\s+per\s+gram', html_content, re.IGNORECASE | re.DOTALL))
            
            rate_24k = None
            rate_22k = None
            
            # Look for 24K and 22K patterns more carefully
            for match in all_currency_matches:
                full_text = html_content[max(0, match.start()-100):match.end()+100]
                
                if '24' in full_text and 'karat' in full_text.lower():
                    rate_str = match.group(1).replace(',', '')
                    try:
                        rate_24k = float(rate_str)
                    except:
                        pass
                elif '22' in full_text and 'karat' in full_text.lower():
                    rate_str = match.group(1).replace(',', '')
                    try:
                        rate_22k = float(rate_str)
                    except:
                        pass
            
            # Alternative: search for specific patterns
            if not rate_24k:
                # Pattern: look for text mentioning "24 Karat" or "24K" followed by ₹XXXXX
                pattern = r'24\s*[Kk](?:arat)?.*?₹\s*([\d,]+)\s*(?:-|gold)'
                match = re.search(pattern, html_content, re.IGNORECASE | re.DOTALL)
                if match:
                    try:
                        rate_24k = float(match.group(1).replace(',', ''))
                    except:
                        pass
            
            if not rate_22k:
                # Pattern: look for text mentioning "22 Karat" or "22K" followed by ₹XXXXX
                pattern = r'22\s*[Kk](?:arat)?.*?₹\s*([\d,]+)\s*(?:-|gold)'
                match = re.search(pattern, html_content, re.IGNORECASE | re.DOTALL)
                if match:
                    try:
                        rate_22k = float(match.group(1).replace(',', ''))
                    except:
                        pass
            
            # If standard parsing fails, look for the heading and extract nearby numbers
            if not rate_24k or not rate_22k:
                # Find "24 Karat Gold Price In India" section
                idx_24k = html_content.find('24 Karat')
                idx_22k = html_content.find('22 Karat')
                
                if idx_24k != -1:
                    section_24k = html_content[idx_24k:idx_24k+500]
                    nums = re.findall(r'₹\s*([\d,]+)', section_24k)
                    if nums:
                        try:
                            rate_24k = float(nums[0].replace(',', ''))
                        except:
                            pass
                
                if idx_22k != -1:
                    section_22k = html_content[idx_22k:idx_22k+500]
                    nums = re.findall(r'₹\s*([\d,]+)', section_22k)
                    if nums:
                        try:
                            rate_22k = float(nums[0].replace(',', ''))
                        except:
                            pass
            
            # If we found rates, return them
            if rate_24k and rate_22k:
                return {
                    'rate_22k': rate_22k,
                    'rate_24k': rate_24k,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'goldpriceindia.com'
                }
            
            logger.warning(f"Could not extract rates - 24K: {rate_24k}, 22K: {rate_22k}")
            return None
        
        except Exception as e:
            logger.error(f"Error parsing goldpriceindia.com: {str(e)}")
            return None
    
    @staticmethod
    def _parse_previous_day_rates(html_content: str) -> dict:
        """
        Parse previous day gold rates from the 10-day history table.
        The table shows daily rates. We extract the first row which is yesterday's data.
        
        Args:
            html_content: HTML content from the website
        
        Returns:
            Dictionary with 22K and 24K rates per gram from previous day
        """
        try:
            # Look for the "Last 10 Days Gold Price Chart" section and find the first date entry
            # Pattern: Date | ₹XXXXX | ₹XXXXX | Change
            # Example: Mon, 02 Mar 2026 | ₹167,505▲ | ₹153,546▲ | +5465 (3.26%)
            
            # Find the history section
            history_start = html_content.find('Last 10 Days Gold Price')
            if history_start == -1:
                logger.warning("Could not find 10-day history section")
                return {}
            
            # Look for date patterns in the history
            # Pattern: Mon/Tue/Wed/etc, DD Mon YYYY or just date | ₹XXXXX | ₹XXXXX
            history_section = html_content[history_start:history_start+3000]
            
            # Extract the first date entry after "Today"
            # Look for pattern: Mon, 02 Mar 2026 | ₹167,505▲ | ₹153,546▲
            pattern = r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[^|]*\s*\|\s*₹\s*([\d,]+)[\▲▼]*\s*\|\s*₹\s*([\d,]+)[\▲▼]*'
            
            matches = re.finditer(pattern, history_section, re.IGNORECASE)
            first_date_match = None
            for match in matches:
                first_date_match = match
                break  # Get only the first match (previous day or most recent)
            
            if first_date_match:
                # The first match is typically the most recent historical entry (yesterday)
                # Format: ₹XXXXX (24K) | ₹XXXXX (22K)
                rate_24k_str = first_date_match.group(1).replace(',', '')
                rate_22k_str = first_date_match.group(2).replace(',', '')
                
                # These are per 10 gram, convert to per gram
                rate_24k = float(rate_24k_str) / 10
                rate_22k = float(rate_22k_str) / 10
                
                return {
                    'rate_22k': rate_22k,
                    'rate_24k': rate_24k,
                    'source': 'goldpriceindia.com_history'
                }
            
            logger.warning("Could not extract previous day rates from history table")
            return {}
        
        except Exception as e:
            logger.error(f"Error parsing previous day rates: {str(e)}")
            return {}
    

    def load_previous_rates(self) -> dict:
        """
        Load gold rates from previous day.
        
        Returns:
            Dictionary with previous day's rates, or empty dict if file doesn't exist
        """
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    logger.info("Loaded previous gold rates from file")
                    return data
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load previous rates: {str(e)}")
                return {}
        
        return {}
    
    def save_current_rates(self, data: dict) -> None:
        """
        Save current gold rates to file for future reference.
        
        Args:
            data: Gold rate data to save
        """
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info("Saved current gold rates to file")
        except IOError as e:
            logger.error(f"Failed to save gold rates: {str(e)}")
    
    def get_rates_with_comparison(self) -> dict:
        """
        Fetch current gold rates and previous day rates from website.
        Compare them to calculate changes.
        
        Returns:
            Dictionary with current rates and comparison data
        """
        try:
            # Fetch the webpage once
            logger.info(f"Fetching gold rates and history from {self.api_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            html_content = None
            try:
                response = self.session.get(
                    self.api_url, 
                    timeout=self.timeout,
                    verify=False,
                    headers=headers
                )
                response.raise_for_status()
                html_content = response.text
            except requests.RequestException as e:
                logger.error(f"Failed to fetch from website: {str(e)}")
                logger.info("Will use previously saved data for comparison")
            
            if html_content:
                # Parse current rates from website
                current_rates = self._parse_goldpriceindia(html_content)
                # Parse previous day rates from history table
                previous_rates = self._parse_previous_day_rates(html_content)
                
                if not current_rates:
                    logger.warning("Could not parse current rates from website, using mock data")
                    current_rates = self._get_mock_data()
                
                if not previous_rates:
                    logger.warning("Could not parse previous rates from history, loading from file")
                    previous_rates = self.load_previous_rates()
            else:
                # Website is not accessible
                logger.warning("Website not accessible, using saved data")
                # Load current rates from file as fallback
                saved_rates = self.load_previous_rates()
                # Use mock as current if saved data exists
                if saved_rates:
                    current_rates = self._get_mock_data()  # Use fresh mock for current
                    previous_rates = saved_rates  # Use saved data as previous
                    logger.info(f"Using saved previous rates from file")
                else:
                    # No saved data, use mock for both
                    current_rates = self._get_mock_data()
                    previous_rates = {}
                    logger.warning("No saved data found, using mock data only")
            
            # Extract and process rates
            processed_data = self._process_rates(current_rates, previous_rates)
            
            # Save current rates for future reference (next day's comparison)
            self.save_current_rates(current_rates)
            
            return processed_data
        except Exception as e:
            logger.error(f"Error getting rates with comparison: {str(e)}")
            raise
    
    @staticmethod
    def _process_rates(current: dict, previous: dict) -> dict:
        """
        Process rate data to show rates in both per gram and per 10 gram.
        
        Args:
            current: Current rate data from API (per gram)
            previous: Previous rate data (per gram)
        
        Returns:
            Processed rate data with trends and multiple denominations
        """
        # Get rates per gram from current data
        current_22k = current.get('rate_22k', 0)
        current_24k = current.get('rate_24k', 0)
        
        # Get rates per gram from previous data
        previous_22k = previous.get('rate_22k', 0) if previous else 0
        previous_24k = previous.get('rate_24k', 0) if previous else 0
        
        # Calculate changes for 22K
        change_22k = current_22k - previous_22k
        change_percent_22k = ((change_22k / previous_22k) * 100) if previous_22k > 0 else 0
        
        # Calculate changes for 24K
        change_24k = current_24k - previous_24k
        change_percent_24k = ((change_24k / previous_24k) * 100) if previous_24k > 0 else 0
        
        return {
            'timestamp': datetime.now().isoformat(),
            'unit': 'INR',
            'rates': {
                '24K': {
                    'current_per_gram': round(current_24k, 2),
                    'current_per_10gram': round(current_24k * 10, 2),
                    'previous_per_gram': round(previous_24k, 2),
                    'previous_per_10gram': round(previous_24k * 10, 2),
                    'change': round(change_24k, 2),
                    'change_per_10gram': round(change_24k * 10, 2),
                    'change_percent': round(change_percent_24k, 2),
                    'trend': '↑' if change_24k > 0 else ('↓' if change_24k < 0 else '→')
                },
                '22K': {
                    'current_per_gram': round(current_22k, 2),
                    'current_per_10gram': round(current_22k * 10, 2),
                    'previous_per_gram': round(previous_22k, 2),
                    'previous_per_10gram': round(previous_22k * 10, 2),
                    'change': round(change_22k, 2),
                    'change_per_10gram': round(change_22k * 10, 2),
                    'change_percent': round(change_percent_22k, 2),
                    'trend': '↑' if change_22k > 0 else ('↓' if change_22k < 0 else '→')
                }
            }
        }
