import argparse
from .crawler import AuditSpider, check_links
from .seo import analyze_seo
from .pagespeed import pagespeed_audit
from .report import generate_csv_report

def main():
    parser = argparse.ArgumentParser(description="Website Audit CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Crawl command
    crawl_parser = subparsers.add_parser("crawl")
    crawl_parser.add_argument("url", help="URL to crawl")

    # SEO command
    seo_parser = subparsers.add_parser("seo")
    seo_parser.add_argument("url", help="URL to analyze SEO")

    args = parser.parse_args()

    if args.command == "crawl":
        print(f"Checking links for {args.url} ...")
        results = check_links([args.url])
        print(results)
        generate_csv_report(results)
    elif args.command == "seo":
        print(f"Analyzing SEO for {args.url} ...")
        seo = analyze_seo(args.url)
        print(seo)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
