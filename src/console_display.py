"""Console display module for gold rate data."""
from datetime import datetime
from tabulate import tabulate
from src.logger import logger


class ConsoleDisplay:
    """Handle console display of gold rates."""
    
    @staticmethod
    def display_rates(rate_data: dict) -> None:
        """
        Display gold rates in a professional tabular format.
        Shows rates per gram and per 10 gram.
        
        Args:
            rate_data: Dictionary with rate information
        """
        try:
            rates = rate_data.get('rates', {})
            timestamp = rate_data.get('timestamp', '')
            
            print("\n" + "="*100)
            print(f"  GOLD RATE UPDATE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*100)
            
            # Per Gram Rates Table
            print("\n🔹 PER GRAM (1gm):")
            print("-"*100)
            table_data_gram = []
            for carat, data in rates.items():
                trend = data.get('trend', '→')
                current = data.get('current_per_gram', 0)
                previous = data.get('previous_per_gram', 0)
                change = data.get('change', 0)
                change_percent = data.get('change_percent', 0)
                
                change_str = f"{trend} {change:+.2f}"
                change_percent_str = f"{change_percent:+.2f}%"
                
                table_data_gram.append([
                    f"{carat} Carat",
                    f"₹ {current:,.2f}",
                    f"₹ {previous:,.2f}",
                    change_str,
                    change_percent_str
                ])
            
            headers = ["Carat Type", "Current", "Previous", "Change (₹)", "Change %"]
            print(tabulate(table_data_gram, headers=headers, tablefmt='grid', stralign='center'))
            
            # Per 10 Gram Rates Table
            print("\n🔹 PER 10 GRAMS (10gm):")
            print("-"*100)
            table_data_10gram = []
            for carat, data in rates.items():
                trend = data.get('trend', '→')
                current = data.get('current_per_10gram', 0)
                previous = data.get('previous_per_10gram', 0)
                change = data.get('change_per_10gram', 0)
                change_percent = data.get('change_percent', 0)
                
                change_str = f"{trend} {change:+.2f}"
                change_percent_str = f"{change_percent:+.2f}%"
                
                table_data_10gram.append([
                    f"{carat} Carat",
                    f"₹ {current:,.2f}",
                    f"₹ {previous:,.2f}",
                    change_str,
                    change_percent_str
                ])
            
            print(tabulate(table_data_10gram, headers=headers, tablefmt='grid', stralign='center'))
            print("="*100 + "\n")
            
            logger.info("Rates displayed successfully")
            
        except Exception as e:
            logger.error(f"Error displaying rates: {str(e)}")
            raise
    
    @staticmethod
    def display_analysis(rate_data: dict) -> str:
        """
        Generate text analysis of gold rates with per gram and per 10 gram breakdown.
        
        Args:
            rate_data: Dictionary with rate information
        
        Returns:
            Formatted analysis string
        """
        try:
            rates = rate_data.get('rates', {})
            
            analysis_lines = [
                "\n📊 GOLD RATE ANALYSIS",
                "-" * 80,
            ]
            
            for carat, data in rates.items():
                trend = data.get('trend', '→')
                current_gram = data.get('current_per_gram', 0)
                current_10gram = data.get('current_per_10gram', 0)
                previous_gram = data.get('previous_per_gram', 0)
                previous_10gram = data.get('previous_per_10gram', 0)
                change = data.get('change', 0)
                change_10gram = data.get('change_per_10gram', 0)
                change_percent = data.get('change_percent', 0)
                
                trend_text = "INCREASED ⬆️" if trend == "↑" else ("DECREASED ⬇️" if trend == "↓" else "UNCHANGED →")
                
                analysis_lines.append(f"\n{carat} Carat Gold: {trend_text}")
                analysis_lines.append(f"  Per Gram:")
                analysis_lines.append(f"    Current: ₹ {current_gram:,.2f}")
                analysis_lines.append(f"    Previous: ₹ {previous_gram:,.2f}")
                analysis_lines.append(f"    Change: {change:+.2f} INR ({change_percent:+.2f}%)")
                analysis_lines.append(f"  Per 10 Grams:")
                analysis_lines.append(f"    Current: ₹ {current_10gram:,.2f}")
                analysis_lines.append(f"    Previous: ₹ {previous_10gram:,.2f}")
                analysis_lines.append(f"    Change: {change_10gram:+.2f} INR ({change_percent:+.2f}%)")
            
            analysis_lines.append("\n" + "-" * 80)
            
            return "\n".join(analysis_lines)
        
        except Exception as e:
            logger.error(f"Error generating analysis: {str(e)}")
            raise
