# Οδηγός: φτιάξε το dashboard στο Power BI (περίπου 3–4 ώρες)

Τα δεδομένα, ο κώδικας Python, οι μετρήσεις DAX και το README είναι έτοιμα. Αυτό που μένει είναι να φτιάξεις εσύ το dashboard στο Power BI. Είναι το κομμάτι που θα σε ρωτήσουν στη συνέντευξη, οπότε πρέπει να το έχεις κάνει με τα χέρια σου.

## 0. Προετοιμασία (15')

1. Κατέβασε το **Power BI Desktop** (δωρεάν) από το Microsoft Store στα Windows.
2. Αποσυμπίεσε το `olist-sales-dashboard.zip` σε έναν φάκελο, π.χ. `Documents\olist-sales-dashboard`.
3. Τα έτοιμα δεδομένα είναι στο `data\processed\`: `orders.csv` και `order_items.csv`.

## 1. Φόρτωση δεδομένων (15')

1. Power BI → **Get data → Text/CSV** → διάλεξε το `orders.csv` → **Transform Data**.
2. Στο Power Query έλεγξε τους τύπους των στηλών:
   - `order_date` → **Date**
   - `revenue`, `freight` → **Decimal number**
   - `items`, `review_score`, `delivery_days` → **Whole number**
   - `late` → **True/False**
3. Το ίδιο για το `order_items.csv` (`price`, `freight_value` → Decimal number).
4. **Close & Apply**.

## 2. Μοντέλο δεδομένων (15')

1. Φτιάξε τον πίνακα **Calendar** με τον κώδικα από το `dax_measures.md` (Modeling → New table).
2. Στον Calendar: πάτα τη στήλη `Month` → **Sort by column → MonthNo**. Μετά **Mark as date table**.
3. Στην προβολή **Model**, σύρε:
   - `Calendar[Date]` → `orders[order_date]`
   - `orders[order_id]` → `order_items[order_id]` (ένα προς πολλά)

## 3. Μετρήσεις DAX (20')

Δημιούργησε όλες τις μετρήσεις από το `dax_measures.md` (New measure → επικόλληση). Μορφοποίηση:
- `Revenue`, `Avg Order Value` → νόμισμα R$
- `Late Delivery %`, `Revenue MoM %` → ποσοστό

**Έλεγχος:** σε μια κάρτα, το `Revenue` πρέπει να δείχνει περίπου **13,54M** και το `Late Delivery %` περίπου **6,8%**. Αν δείχνει κάτι άλλο, κάτι πήγε στραβά στους τύπους των στηλών.

## 4. Σελίδα 1: Overview (45')

- 4 **Cards**: Revenue, Orders, Avg Order Value, Avg Review Score
- **Line chart**: άξονας `Calendar[Month]`, τιμές `Revenue` → φαίνεται η κορυφή τον Νοέμβριο του 2017 (Black Friday)
- **Bar chart**: `customer_state` × `Revenue`, top 10
- **Slicers**: `Calendar[Date]` (between) και `customer_state`

## 5. Σελίδα 2: Products (30')

- **Bar chart**: `order_items[category]` × `Revenue` (top 10)
- **Table**: category, Items Sold, Revenue, Avg Item Price
- **Donut**: `payment_type` × `Orders`

## 6. Σελίδα 3: Delivery & Satisfaction (45')

- **Cards**: Late Delivery %, Avg Delivery Days
- **Line chart**: `Calendar[Month]` × `Late Delivery %`
- **Clustered column**: άξονας `orders[late]`, τιμή `Avg Review Score` → **το κεντρικό εύρημα: 4,3 έναντι 2,3 αστέρια**
- **Bar chart**: `customer_state` × `Avg Delivery Days`

## 7. Εμφάνιση (20')

- Ίδια χρώματα σε όλες τις σελίδες (View → Themes)
- Τίτλος σε κάθε σελίδα και κάθε γράφημα
- Τα slicers στην ίδια θέση σε κάθε σελίδα (View → Sync slicers)

## 8. Ανέβασμα στο GitHub (20')

1. Αποθήκευσε ως `olist_dashboard.pbix` στον φάκελο του project.
2. Πάρε screenshot της σελίδας Overview → `images\dashboard_overview.png` (το README το περιμένει με αυτό το όνομα).
3. Στο GitHub: **New repository** → όνομα `olist-sales-dashboard` → Public → **Create**.
4. **uploading an existing file** → σύρε μέσα όλα τα αρχεία και φακέλους **εκτός από τον `data\raw`** → **Commit**.
   (Αν ένα αρχείο είναι πάνω από 25MB, ανέβασέ το με GitHub Desktop.)

## Μετά

Πες μου όταν ανέβει. Θα προσθέσω το project στο βιογραφικό και το **Power BI** στις δεξιότητες. Στη συνέντευξη να είσαι έτοιμος να πεις:
- **Τι έφτιαξες:** «Dashboard για 99 χιλιάδες παραγγελίες e-commerce. Καθάρισα τα δεδομένα σε Python και έστησα μοντέλο με DAX στο Power BI.»
- **Τι βρήκες:** «Οι καθυστερημένες παραδόσεις ρίχνουν τη βαθμολογία από 4,3 σε 2,3 αστέρια. Επίσης, μόνο το 3% των πελατών ξαναγοράζει.»
- **Τι θα πρότεινες:** «Βελτίωση των παραδόσεων στις πολιτείες με τους μεγαλύτερους χρόνους, και πρόγραμμα επιβράβευσης για να ξαναγοράζουν οι πελάτες.»
