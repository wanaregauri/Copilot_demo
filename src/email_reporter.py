"""Email module for sending gold rate reports."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from src.config import config
from src.logger import logger


class EmailReporter:
    """Handle email notifications for gold rate updates."""
    
    def __init__(self):
        """Initialize email reporter with configuration."""
        self.sender = config.EMAIL_SENDER
        self.password = config.EMAIL_PASSWORD
        self.recipient = config.EMAIL_RECIPIENT
        self.smtp_server = config.SMTP_SERVER
        self.smtp_port = config.SMTP_PORT
    
    def _validate_config(self) -> bool:
        """
        Validate email configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not all([self.sender, self.password, self.recipient]):
            logger.warning("Email configuration incomplete. Please set environment variables.")
            return False
        return True
    
    def create_html_report(self, rate_data: dict) -> str:
        """
        Create HTML-formatted email report with color-coded changes.
        Shows rates per gram and per 10 grams.
        
        Args:
            rate_data: Dictionary with rate information
        
        Returns:
            HTML string for email body
        """
        rates = rate_data.get('rates', {})
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create HTML table rows for per gram
        table_rows_gram = ""
        table_rows_10gram = ""
        
        for carat, data in rates.items():
            trend = data.get('trend', '→')
            current_gram = data.get('current_per_gram', 0)
            previous_gram = data.get('previous_per_gram', 0)
            current_10gram = data.get('current_per_10gram', 0)
            previous_10gram = data.get('previous_per_10gram', 0)
            change = data.get('change', 0)
            change_10gram = data.get('change_per_10gram', 0)
            change_percent = data.get('change_percent', 0)
            
            # Color coding based on trend
            color = '#2ecc71' if trend == '↑' else ('#e74c3c' if trend == '↓' else '#95a5a6')
            trend_symbol = '📈' if trend == '↑' else ('📉' if trend == '↓' else '➡️')
            
            change_str = f"{change:+.2f} INR ({change_percent:+.2f}%)"
            change_str_10gram = f"{change_10gram:+.2f} INR ({change_percent:+.2f}%)"
            
            # Per gram row
            table_rows_gram += f"""
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 12px; text-align: left; font-weight: bold;">{carat} Carat</td>
                <td style="padding: 12px; text-align: right;">₹ {current_gram:,.2f}</td>
                <td style="padding: 12px; text-align: right;">₹ {previous_gram:,.2f}</td>
                <td style="padding: 12px; text-align: center; color: {color}; font-weight: bold;">
                    {trend_symbol} {change_str}
                </td>
            </tr>
            """
            
            # Per 10 gram row
            table_rows_10gram += f"""
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 12px; text-align: left; font-weight: bold;">{carat} Carat</td>
                <td style="padding: 12px; text-align: right;">₹ {current_10gram:,.2f}</td>
                <td style="padding: 12px; text-align: right;">₹ {previous_10gram:,.2f}</td>
                <td style="padding: 12px; text-align: center; color: {color}; font-weight: bold;">
                    {trend_symbol} {change_str_10gram}
                </td>
            </tr>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 30px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 6px;
                    margin-bottom: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .header p {{
                    margin: 5px 0 0 0;
                    font-size: 14px;
                    opacity: 0.9;
                }}
                .timestamp {{
                    color: #7f8c8d;
                    font-size: 12px;
                    margin-bottom: 20px;
                    text-align: center;
                }}
                .section-title {{
                    font-size: 16px;
                    font-weight: bold;
                    color: #34495e;
                    margin-top: 25px;
                    margin-bottom: 10px;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 8px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                th {{
                    background-color: #34495e;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ecf0f1;
                    font-size: 12px;
                    color: #7f8c8d;
                    text-align: center;
                }}
                .disclaimer {{
                    background-color: #ecf0f1;
                    padding: 10px;
                    border-radius: 4px;
                    margin-top: 15px;
                    font-size: 11px;
                    color: #34495e;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💰 Gold Rate Update Report</h1>
                    <p>Daily Price Comparison (Per Gram & Per 10 Grams)</p>
                </div>
                
                <div class="timestamp">
                    Generated on {timestamp}
                </div>
                
                <div class="section-title">Per Gram (1 gm)</div>
                <table>
                    <thead>
                        <tr>
                            <th>Carat Type</th>
                            <th>Current Rate</th>
                            <th>Previous Rate</th>
                            <th>Change</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows_gram}
                    </tbody>
                </table>
                
                <div class="section-title">Per 10 Grams (10 gm)</div>
                <table>
                    <thead>
                        <tr>
                            <th>Carat Type</th>
                            <th>Current Rate</th>
                            <th>Previous Rate</th>
                            <th>Change</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows_10gram}
                    </tbody>
                </table>
                
                <div class="footer">
                    <p><strong>Data Source:</strong> goldpriceindia.com</p>
                    <p><strong>Rates are in INR (Indian Rupees)</strong></p>
                    <div class="disclaimer">
                        ⚠️ Disclaimer: This report is for informational purposes only. 
                        Gold prices are subject to market fluctuations and rates may vary by dealer. 
                        Please verify current rates with local dealers before making any transactions.
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def send_email(self, rate_data: dict) -> bool:
        """
        Send HTML-formatted email report with gold rate data.
        
        Args:
            rate_data: Dictionary with rate information
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self._validate_config():
            return False
        
        try:
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Gold Rate Update - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = self.sender
            msg['To'] = self.recipient
            
            # Create HTML content
            html_content = self.create_html_report(rate_data)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            logger.info(f"Sending email to {self.recipient}")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)
            
            logger.info("Email sent successfully")
            return True
        
        except smtplib.SMTPAuthenticationError:
            logger.error("Email authentication failed. Check credentials in .env file")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
