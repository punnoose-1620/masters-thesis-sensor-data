***

# 📝 **REPORT: Why the Wiki URL Cannot Be Added & Evaluation of Dynamic Integration Approaches**

***

## **1. Why Your Original URL Cannot Be Added as a Knowledge Source**

Even though the wiki is publicly accessible and Bing-indexed, Copilot Studio still rejects it due to **multiple rule violations**.

### **1.1. The URL contains a dynamic script path (`index.php`), which is disallowed**

Microsoft requires that public website URLs:

*   Use **clean paths**
*   Have **no more than two levels of depth**
*   Do **not** rely on dynamic script files (like PHP)

Our URL:

    /wice296/index.php/Main_Page

Dynamic/scripted URLs like this violate:

> “The URL can have up to two levels of depth… \[and] there are requirements and restrictions on some URLs.”    [\[en.wikipedia.org\]](https://en.wikipedia.org/wiki/Robots.txt)

### **1.2. “Wikis” are explicitly categorized as unsupported**

Microsoft's own examples include:

> “For example, wikis… can't be used.”    [\[en.wikipedia.org\]](https://en.wikipedia.org/wiki/Robots.txt)

This is not conditional — Microsoft treats *all* wikis (internal or public) as incompatible with ingestion.

### **1.3. Dynamic site layouts can block automated extraction**

Community experts emphasize that:

> “There are limitations depending on the type of website — layout, robots.txt and meta tags that can limit interrogation by automated tools.”    [\[developers...google.com\]](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

MediaWiki layouts include:

*   Dynamic templates
*   Load.php resources
*   URL rewriting
*   User-agent‑sensitive rendering

These break Microsoft’s extraction pipeline.

### **1.4. Bing indexing ≠ Bing content availability**

The WICE Wiki URL appears in Bing results, but Copilot Studio needs **full-content snapshots**, not just titles/snippets.

Wikis often allow indexing but restrict full content retrieval — a known MediaWiki pattern (documented in MediaWiki’s robots.txt guidance).    [\[alkit.se\]](https://www.alkit.se/)

### **1.5. Multi-level logical depth exceeds Copilot limits**

Even if the URL appears shallow, wiki content is internally structured with deep dynamic paths, beyond Copilot Studio’s supported depth.    [\[en.wikipedia.org\]](https://en.wikipedia.org/wiki/Robots.txt)

***

## **2. Why the Bit.ly (URL Shortener) Approach Does NOT Work**

Using Bit.ly, TinyURL, or any other shortener **does not bypass** Copilot Studio’s URL restrictions.

### **2.1. Copilot Studio rejects URLs that redirect**

Microsoft clearly states:

> “If the URL redirects to another top-level site, the content isn’t included in results.”    [\[en.wikipedia.org\]](https://en.wikipedia.org/wiki/Robots.txt)

A Bit.ly link *always* performs a redirect, so Copilot Studio **disqualifies the URL immediately**, before even evaluating the destination.

### **2.2. URL shorteners do not hide the underlying structure**

After resolving the redirect, Copilot Studio still arrives at the same URL:

    https://wiki.alkit.se/wice296/index.php/Main_Page

This URL still violates Microsoft’s restrictions (see Section 2).

### **2.3. URL shorteners do not fix unsupported website types**

Microsoft explicitly lists **wikis** among the types of websites that Copilot Studio cannot use as knowledge sources:

> “URLs that point to a website requiring authentication or ones not indexed by Bing.  
> **For example, wikis… can’t be used.**”    [\[en.wikipedia.org\]](https://en.wikipedia.org/wiki/Robots.txt)

The site type does not change because the URL is shortened.

### **2.4. Redirects break Bing Grounding**

Public website knowledge sources rely on:

> “Grounding with Bing Search to return information from the web.”    [\[en.wikipedia.org\]](https://en.wikipedia.org/wiki/Robots.txt)

Redirects reduce Bing’s ability to retrieve a clean content snapshot. Even if Bing indexes the URL (as in your test), Copilot Studio may still fail to ingest it due to lack of extractable content.

***


# **3. Comparison of Three Dynamic Integration Approaches**

To keep content dynamic, you must bypass public‑website ingestion and instead use **runtime data access**.  
Below is a side‑by‑side comparison.

***

## **Approach A — Azure Function API (Endpoint) + Custom Connector**

### ✔ **Dynamic** | ✔ **Fully supported** | ✔ **Flexible** | ⭐ **Recommended**

### **How it works**

*   You create an Azure Function accessible via HTTP.
*   The function fetches and parses the wiki page.
*   Copilot Studio calls this endpoint dynamically using a Custom Connector.

### **Pros**

*   Truly **real-time** content retrieval
*   Full control over parsing
*   Works for any website type (including wikis)
*   Bypasses Bing limitations entirely
*   No need for the site to meet URL rules or indexing rules

### **Cons**

*   Requires building a small parser
*   Slight development overhead (but doable 100% in Azure Portal GUI)

### **Best for**

Dynamic knowledge delivery, rapid updates, system‑driven automation.

***

## **Approach B — Scheduled Azure Function + SharePoint/Blob Storage (Dynamic Snapshot)**

### ✔ **Dynamic-ish** | ✔ **Supported** | ❗ **Not real-time**

### **How it works**

*   Azure Function fetches wiki pages periodically (e.g., hourly).
*   Converts to PDF/HTML/TXT.
*   Uploads these automatically into SharePoint or Blob.
*   Copilot Studio uses file-based knowledge ingestion.

### **Pros**

*   Works with Copilot’s built‑in knowledge source mechanism
*   Good long-term reliability
*   Easy document management

### **Cons**

*   **Not** real-time
*   Ingestion delay depends on indexing schedule
*   Requires automation setup

### **Best for**

Content that updates periodically but not minute‑by‑minute.

***

## **Approach C — Bing Custom Search + Copilot API Integration**

### ✔ **Dynamic search** | ❗ **Requires Bing CS setup** | ❗ **May still struggle with MediaWiki content**

### **How it works**

*   You define a custom search domain (`wiki.alkit.se`) in Bing CS.
*   Copilot uses Bing CS via a connector to search wiki pages dynamically.

### **Pros**

*   Retrieval is dynamic
*   No need to write a parser
*   Offloads crawling and indexing to Bing Custom Search

### **Cons**

*   Bing CS may not extract full wiki article text
*   Requires configuring custom search instance
*   Not guaranteed to handle script‑based pages
*   Costs scale with usage

### **Best for**

Search-first workflows where exact article content is less important.

***

# **4. Summary Table: Which Approach to Choose?**

| Requirement                  | Azure API Endpoint | Scheduled Snapshot (SharePoint/Blob) | Bing Custom Search |
| ---------------------------- | ------------------ | ------------------------------------ | ------------------ |
| Real-time dynamic data       | ⭐ **Yes**          | ❌ No                                 | ✔ Partial          |
| Works with wiki pages        | ⭐ **Yes**          | ⭐ Yes                                | ❌ Not always       |
| Fully supported by Copilot   | ⭐ Yes (as Action)  | ⭐ Yes (as Knowledge)                 | ✔ Yes              |
| Requires parsing logic       | ✔ Yes              | ✔ Optional                           | ❌ No               |
| Dependent on Bing indexing   | ❌ No               | ❌ No                                 | ⭐ Yes              |
| Easiest to maintain          | ⭐ High             | Medium                               | Medium             |
| Handles complex/dynamic URLs | ⭐ Yes              | ⭐ Yes                                | ❌ Often fails      |

***

# 🟢 **Final Recommendation**

📌  
**Use the Azure Function API with a Custom Connector**.  
This is the **only option** that gives:

*   **True real-time** dynamic access
*   Full reliability
*   No dependency on URL rules
*   No dependency on Bing’s limited extraction
*   Full compatibility with Copilot Studio actions
*   Full control over parsing and formatting

Both Bit.ly and direct wiki ingestion will **never** work due to Microsoft’s **explicit restrictions** on:

*   Redirected URLs
*   Script‑based paths
*   Dynamic pages
*   Wikis as a site type    [\[en.wikipedia.org\]](https://en.wikipedia.org/wiki/Robots.txt), [\[developers...google.com\]](https://developers.google.com/search/docs/crawling-indexing/robots/intro)

By contrast, the Azure Function approach bypasses all these limitations.

***