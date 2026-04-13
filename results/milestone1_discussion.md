# Milestone 1 — Qualitative Evaluation: BM25 vs Semantic Search

## Dataset
Amazon All_Beauty reviews — 70,000 documents indexed using BM25 (rank-bm25) and Semantic Search (all-MiniLM-L6-v2 + ChromaDB).

---

## Queries and Results

### Query 1: "shampoo" *(Easy)*

**BM25 Top 5:**
1. Purple Shampoo And Conditioner Set Blonde Shampoo... — Score: 7.4752 ⭐⭐
2. Purple Shampoo And Conditioner Set Blonde Shampoo... — Score: 7.3476 ⭐⭐⭐⭐⭐
3. Suave Essentials Sunripened Strawberry Shampoo And Conditioner — Score: 7.3436 ⭐
4. Foamie Shampoo Bar Aloe You Vera Much — Score: 7.303 ⭐
5. Excellent Shampoo — Score: 7.2989 ⭐⭐⭐⭐⭐

**Semantic Top 5:**
1. Shampoo Working — Score: 0.5835 ⭐⭐⭐⭐⭐
2. Great Shampoo — Score: 0.5169 ⭐⭐⭐⭐⭐
3. Monat Junior Gentle Shampoo — Score: 0.4929 ⭐⭐⭐⭐⭐
4. The Best — Score: 0.4583 ⭐⭐⭐⭐⭐
5. Excellent — Score: 0.4339 ⭐⭐⭐⭐⭐

---

### Query 2: "lip gloss" *(Easy)*

**BM25 Top 5:**
1. Lotus Pure Organics Natural Lipgloss... — Score: 13.3716 ⭐⭐⭐⭐⭐
2. Bourjois Effect 3D Brillant Lipgloss — Score: 13.3582 ⭐⭐⭐⭐⭐
3. Good Lipgloss — Score: 12.3263 ⭐⭐⭐
4. Butter London Lippy Liquid Lipstick — Score: 12.176 ⭐
5. Lipgloss — Score: 12.1035 ⭐⭐⭐⭐⭐

**Semantic Top 5:**
1. Good Lipgloss — Score: 0.5317 ⭐⭐⭐
2. Lipgloss — Score: 0.4235 ⭐⭐⭐⭐⭐
3. Its A Nice Lipgloss — Score: 0.3461 ⭐⭐⭐
4. My Favorite Lipgloss — Score: 0.3303 ⭐⭐⭐⭐⭐
5. Broadway Vitalip Argan Oil Lip Gloss — Score: 0.3138 ⭐⭐⭐⭐⭐

---

### Query 3: "natural deodorant without aluminum" *(Medium)*

**BM25 Top 5:**
1. Deodorant Vanilla Coconut With Organic Ingredients... Aluminum Free — Score: 22.3826 ⭐⭐⭐⭐⭐
2. Vanicream Aluminum Free Deodorant Gel Formula — Score: 20.7983 ⭐⭐
3. Natural Deodorant Unscented Made With Organic Ingredients... Aluminum Free — Score: 20.6066 ⭐⭐⭐
4. Primal Pit Paste Natural Deodorant Aluminum Free — Score: 20.4733 ⭐⭐⭐⭐⭐
5. Magsol Natural Deodorant... Aluminum Free — Score: 20.2812 ⭐⭐⭐⭐⭐

**Semantic Top 5:**
1. No More Aluminum Deodorant For Me — Score: 0.6427 ⭐⭐⭐⭐⭐
2. Its All Good — Score: 0.6348 ⭐⭐⭐⭐⭐
3. Native Deodorant Natural... Aluminum Free With Baking Soda — Score: 0.6319 ⭐⭐⭐⭐⭐
4. Genuine Authentic German Nivea Deodorant Fresh Pure Aluminum Free — Score: 0.5932 ⭐⭐⭐⭐⭐
5. Genuine Authentic German Nivea Deodorant Fresh Pure Aluminum Free — Score: 0.5932 ⭐⭐⭐⭐⭐

---

### Query 4: "anti-aging serum" *(Medium)*

**BM25 Top 5:**
1. Calily Life Organic Antiaging Retinol Serum — Score: 14.7885 ⭐⭐⭐⭐⭐
2. Boots No7 Restore Renew Skin Care Kit — Score: 14.5939 ⭐⭐⭐⭐⭐
3. Boots No7 Restore Renew Skin Care Kit — Score: 14.4626 ⭐⭐⭐⭐
4. Hotmir Vitamin C Serum For Face... Antiaging — Score: 14.0442 ⭐⭐⭐⭐⭐
5. Bella Versache Hyaluronic Acid Serum Anti Wrinkle — Score: 14.0442 ⭐⭐⭐⭐

**Semantic Top 5:**
1. Nice For Price — Score: 0.4339 ⭐⭐⭐⭐⭐
2. Anti Aging Cream — Score: 0.3883 ⭐⭐⭐⭐⭐
3. Anti Aging Serum The Best Hyaluronic Acid Face Cream — Score: 0.382 ⭐⭐⭐⭐⭐
4. Wake Up With Younger Looking Skin Coenzyme Q10 Multi Peptide Serum — Score: 0.3541 ⭐⭐⭐⭐⭐
5. Eye Vibe Antiaging Eye Serum — Score: 0.3541 ⭐⭐⭐⭐⭐

---

### Query 5: "product for sensitive skin that doesn't cause breakouts" *(Complex)*

**BM25 Top 5:**
1. No Rashes Or Breakouts — Score: 22.7098 ⭐⭐⭐⭐⭐
2. Five Stars — Score: 22.3754 ⭐⭐⭐⭐⭐
3. Bali Secrets All Natural Deodorant... — Score: 20.9338 ⭐
4. Amazing — Score: 20.2849 ⭐⭐⭐⭐⭐
5. Vigui Ponds Pure Detox — Score: 20.068 ⭐⭐⭐⭐⭐

**Semantic Top 5:**
1. I Have Very Sensitive Skin — Score: 0.5037 ⭐
2. Gret Product — Score: 0.4537 ⭐⭐⭐⭐⭐
3. Ive Never Had Bad Skin Before — Score: 0.3838 ⭐⭐⭐⭐⭐
4. Not For Super Sensitive Skin — Score: 0.3812 ⭐⭐⭐
5. Just What You Need For Sensitive Skin — Score: 0.3649 ⭐⭐⭐⭐⭐

---

### Query 6: "volumizing conditioner for fine hair" *(Medium)*

**BM25 Top 5:**
1. Argan Oil Shampoo And Conditioner Set... Volumizing — Score: 20.9581 ⭐⭐⭐⭐⭐
2. Philip Kingsley Bodybuilding Weightless Conditioner Volumizing For Fine Limp Hair — Score: 20.94 ⭐⭐⭐⭐⭐
3. Gliss Hair Repair Extra Volume Shampoo Conditioner Set — Score: 20.2104 ⭐⭐⭐⭐⭐
4. Voloom Shine On Dry Conditioner... Volumizing Natural Hair — Score: 20.0212 ⭐⭐⭐⭐⭐
5. 15 Pieces Volumizing Hair Root Clip — Score: 19.4877 ⭐

**Semantic Top 5:**
1. A Very Good Conditioner — Score: 0.4174 ⭐⭐⭐⭐⭐
2. This Conditioner Really Works — Score: 0.4136 ⭐⭐⭐⭐⭐
3. Voloom Shine On Dry Conditioner... Volumizing Natural Hair — Score: 0.4054 ⭐⭐⭐⭐⭐
4. Ikoo Dont Apologize Volumizing Conditioner For Fine Thin Or Flat Hair — Score: 0.4034 ⭐⭐⭐⭐⭐
5. Ikoo Dont Apologize Volumizing Conditioner For Fine Thin Or Flat Hair — Score: 0.4034 ⭐⭐⭐

---

### Query 7: "long lasting red lipstick" *(Medium)*

**BM25 Top 5:**
1. Besame Cosmetics Forever Red Lipstick 1925... Long Lasting — Score: 22.8878 ⭐⭐⭐⭐⭐
2. 20Pcs Tattoo Lipstick Cotton Swab... Long Lasting... Orange Red — Score: 20.2198 ⭐⭐⭐⭐⭐
3. Dollup Beauty The Perfect Red Lipstick... Long Lasting Waterproof — Score: 19.7203 ⭐⭐⭐⭐⭐
4. Tattoo Lipstick Lip Gloss Kit Long Lasting Waterproof... Rose Red — Score: 19.5737 ⭐⭐⭐⭐
5. 20 Pcs Tattoo Lipstick Swab... Long Lasting... Haze Red — Score: 19.5364 ⭐

**Semantic Top 5:**
1. Besame Cosmetics Forever Red Lipstick 1925... Long Lasting — Score: 0.5953 ⭐⭐⭐⭐⭐
2. Besame Cosmetics Forever Red Lipstick 1925... Long Lasting — Score: 0.5869 ⭐⭐⭐⭐⭐
3. Besame Cosmetics Forever Red Lipstick 1925... Long Lasting — Score: 0.5158 ⭐⭐⭐⭐
4. Mynena Long Lasting Liquid Matte Lipstick Kit — Score: 0.4916 ⭐⭐⭐⭐⭐
5. Besame Cosmetics Forever Red Lipstick 1925... Long Lasting — Score: 0.5158 ⭐⭐⭐⭐⭐

---

### Query 8: "sunscreen that doesn't leave white cast" *(Complex)*

**BM25 Top 5:**
1. Fascy Lab Green Korean Sunscreen SPF 50 — Score: 24.8643 ⭐⭐⭐⭐⭐
2. Great Physical Sunscreen — Score: 24.1017 ⭐⭐⭐⭐
3. Rohto Skin Aqua UV Super Moisture Gel SPF50 — Score: 21.1352 ⭐⭐⭐⭐⭐
4. Tropic Labs Smart Screen Broad Spectrum SPF 22 — Score: 20.1965 ⭐⭐⭐⭐⭐
5. Rohto Skin Aqua UV Super Moisture Gel SPF50 — Score: 19.8846 ⭐⭐⭐⭐⭐

**Semantic Top 5:**
1. Caribbean Sol SPF 30 Sunscreen — Score: 0.3878 ⭐⭐⭐⭐
2. Badger SPF 35 Clear Zinc Sport Sunscreen — Score: 0.3668 ⭐⭐⭐⭐⭐
3. Mineral Sun Block By Disco For Men SPF 30 — Score: 0.3299 ⭐⭐⭐⭐
4. Safe Harbor Natural Suncare Sensitive Lotion SPF 50 — Score: 0.3291 ⭐
5. Rohto Skin Aqua UV Super Moisture Gel SPF50 — Score: 0.3201 ⭐⭐⭐⭐⭐

---

### Query 9: "gift set for mom" *(Easy)*

**BM25 Top 5:**
1. Calgon Take Me Away 4 Piece Set Luxury Gift Bag — Score: 20.9479 ⭐⭐⭐⭐⭐
2. Bath Bombs Gift Set... Mothers Day Gifts Ideas For Mom — Score: 20.0877 ⭐⭐⭐⭐⭐
3. 4D Silk Lash Fiber Mascara — Score: 19.831 ⭐⭐⭐⭐⭐
4. Bath Bombs Gift Set... Mothers Day Gifts Ideas For Mom — Score: 19.6323 ⭐⭐⭐⭐⭐
5. Bath Bombs Gift Set... Mothers Day Gifts Ideas For Mom — Score: 19.5021 ⭐⭐⭐⭐⭐

**Semantic Top 5:**
1. Gift Item — Score: 0.4989 ⭐⭐⭐⭐⭐
2. This Was A Christmas Present — Score: 0.3742 ⭐⭐⭐⭐⭐
3. Gift For Gdaughters Class — Score: 0.3569 ⭐⭐⭐⭐
4. Perfect Gift For Mom — Score: 0.3246 ⭐⭐⭐⭐⭐
5. Gift — Score: 0.3131 ⭐⭐⭐⭐⭐

---

### Query 10: "beard oil for grooming" *(Medium)*

**BM25 Top 5:**
1. Timkdle Beard Grooming Kit... Beard Care For Styling — Score: 24.672 ⭐⭐⭐⭐⭐
2. Timkdle Beard Grooming Kit... Beard Care For Styling — Score: 24.672 ⭐⭐⭐⭐⭐
3. Wowax Beard Brush And Comb Set... Beard Grooming Kit — Score: 23.758 ⭐⭐⭐⭐⭐
4. Beard Brush... Perfect For Beard Oil Balm — Score: 23.3393 ⭐⭐⭐⭐
5. Timkdle Beard Grooming Kit — Score: 23.3238 ⭐⭐⭐⭐

**Semantic Top 5:**
1. Detroit Grooming Co Beard Butter Combo — Score: 0.5169 ⭐
2. Jack Black MP 10 Nourishing Oil — Score: 0.5086 ⭐⭐⭐⭐⭐
3. Good Beard Oil — Score: 0.4519 ⭐⭐⭐⭐⭐
4. Detroit Grooming Co Beard Butter Combo Corktown — Score: 0.4486 ⭐⭐⭐⭐⭐
5. American Shaving Co Beard Wash With Sandalwood — Score: 0.4482 ⭐⭐⭐⭐⭐

---

## Discussion: Comparing BM25 and Semantic Search

### Query 1 — "shampoo"
For a simple one-word query, BM25 returned highly specific products with "shampoo" prominently in the title, including purple shampoos and shampoo bars. Semantic search returned results based on review sentiment and general satisfaction, such as "Great Shampoo" and "Shampoo Working." BM25 performed better here because the query is a direct keyword match, there is no need for conceptual understanding.

### Query 3 — "natural deodorant without aluminum"
Both methods performed well, but in different ways. BM25 matched products that explicitly listed "aluminum free" in their titles, returning highly relevant products. Semantic search captured the *intent* of the query by finding reviews that discussed avoiding aluminum for health reasons (e.g., "I was looking for a deodorant that had no aluminum..."). Semantic search is more useful here for users who want to read real user experiences rather than just product names.

### Query 5 — "product for sensitive skin that doesn't cause breakouts"
This complex query exposed a clear weakness in BM25. It latched onto the words "breakouts" and "sensitive skin" in review text, returning a deodorant and bath salts — not skincare products. Semantic search did better at understanding the overall intent, returning reviews specifically about skincare products that were gentle on the skin. Neither method was perfect, but semantic search showed stronger contextual understanding for this natural language query.

### Query 8 — "sunscreen that doesn't leave white cast"
BM25 performed surprisingly well here because "white cast" is a specific technical phrase that appears in reviews, leading it to return highly relevant sunscreen products. Semantic search returned a broader set of sunscreens but with lower confidence scores overall. This shows that when users use niche but consistent beauty terminology, BM25 can be just as effective as semantic search.

### Query 9 — "gift set for mom"
BM25 returned mostly relevant gift sets but also included a mascara product that mentioned "gift for mom" in the review text, a clear false positive from keyword matching. Semantic search struggled more, returning vague results like "Gift" and "Gift Item" with very little specific information. Neither method excelled here, suggesting that gift oriented queries may benefit from additional metadata filtering such as product category.

---

## Summary

| Aspect | BM25 | Semantic Search |
|---|---|---|
| Simple keyword queries | Excellent | Good |
| Specific product names | Excellent | Good |
| Natural language queries | Poor | Good |
| Complex/multi-concept queries | Poor | Better |
| Niche beauty terminology | Good | Moderate |
| Conceptual understanding | None | Strong |
| Speed | Very fast | Slower (embedding required) |

**BM25 strengths:** Fast, reliable for exact keyword matches, works well when the query uses the same terminology as the product title. Best for queries like "purple shampoo" or "aluminum free deodorant."

**Semantic search strengths:** Understands meaning and context, handles natural language queries better, captures user intent even when exact words differ. Best for queries like "product that won't break me out" or "something moisturizing for winter skin."

**Overall recommendation:** A hybrid approach combining both methods would likely yield the best results, using BM25 for precision on specific product queries and semantic search for exploratory or natural language queries.