import requests
from bs4 import BeautifulSoup

url = "https://sinhala.adaderana.lk/sinhala-hot-news.php"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    
    headlines = soup.select('.news-story h2, .news-story a, p.news-title, .hot-news-content a')
    
    news_html_content = ""
    count = 0
    seen_news = set()  # එකතු කරපු පුවත් මතක තබා ගැනීමට (Duplicates වැළැක්වීමට)

    for headline in headlines:
        text = headline.text.strip()
        
        # පුවත හිස් නැතිනම්, දිග අකුරු 15ට වැඩි නම් සහ දැනටමත් එකතු කර නැතිනම් පමණක් ගනී
        if text and len(text) > 15 and text not in seen_news and count < 10:
            count += 1
            seen_news.add(text)  # පුවත මතකයට එකතු කර ගැනීම
            
            news_html_content += f"""
            <div class="news-card">
                <span class="news-number">#{count}</span>
                <p>{text}</p>
            </div>
            """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="si">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🔴 සජීවී සිංහල පුවත් පද්ධතිය</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>

        <header>
            <h1>🔴 සජීවී උණුසුම් පුවත් සිරස්තල</h1>
            <p>Python Web Scraper මඟින් ස්වයංක්‍රීයව යාවත්කාලීන වේ</p>
        </header>

        <main class="news-container">
            {news_html_content}
        </main>

        <footer>
            <p>&copy; 2026 මගේ පුවත් අඩවිය. සියලුම හිමිකම් ඇවිරිණි.</p>
        </footer>

    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_template)
        
    print("SUCCESS_DONE")

except Exception as e:
    print("❌ ගැටලුවක් ඇති විය:", e)
