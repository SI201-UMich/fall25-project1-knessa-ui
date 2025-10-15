import csv
import unittest

# Helper function: convert numeric strings to floats where needed
def coerce_row_types(row_d):
    for col in ("Sales", "Discount"):
        val = row_d[col]
        if val == "" or val is None:   #checks for blank/missing
            row_d[col] = 0.0
        else:
            row_d[col] = float(val)
    return row_d

# Load
def load_superstore(csv_file):
    data = []
    with open(csv_file, "r", newline="") as inFile:
        csv_r = csv.reader(inFile)
        headers = [h.strip() for h in next(csv_r)]
        idx = {h: i for i, h in enumerate(headers)}

        for row in csv_r:
            if len(row) < len(headers):
                continue
            # include every column
            d = {h: row[i].strip() for h, i in idx.items()}
            d = coerce_row_types(d)
            data.append(d)
    return data

class project1_test(unittest.TestCase):
    def setUp(self):
        self.data = load_superstore('testfile.csv')
        self.avg_disc = avg_discount_by_category(self.data)
        self.sales_summary = total_sales_by_shipmode_and_segment(self.data)

# tests for avg_discount_by_category
    def test_avg_discount_returns_dict(self):
        # return a dictionary where keys = category names and values = weighted average discounts (%)
        self.assertIsInstance(self.avg_disc, dict)
        for v in self.avg_disc.values():
            self.assertIsInstance(v, float)

    def test_avg_discount_categories_exist(self):
        # Check that all known categories from the dataset are in the output
        expected_cats = {"Furniture", "Office Supplies", "Technology"}
        for cat in expected_cats:
            self.assertIn(cat, self.avg_disc)

    def test_avg_discount_values_within_range(self):
        #Weighted average discounts should be between 0 and 100
        for value in self.avg_disc.values():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 100.0)

    def test_avg_discount_skips_blank_category(self):
        #Rows with missing or blank categories should be skipped
        self.assertNotIn("", self.avg_disc)

    def test_avg_discount_handles_missing_numeric_values(self):
        #Missing numeric values should be treated as 0.0 after coercion
        for r in self.data:
            self.assertIsInstance(r["Sales"], float)
            self.assertIsInstance(r["Discount"], float)

#tests for total_sales_by_shipmode_and_segment
    def test_total_sales_returns_dict(self):
        #return a nested dictionary where top-level keys = Ship Modes, inner keys = Segments, and values = total sales
        self.assertIsInstance(self.sales_summary, dict)
        for seg_dict in self.sales_summary.values():
            self.assertIsInstance(seg_dict, dict)
            for v in seg_dict.values():
                self.assertIsInstance(v, float)

    def test_total_sales_expected_shipmodes_exist(self):
        #Known ship modes from the dataset should appear as top level keys
        expected_modes = {"First Class", "Second Class", "Standard Class", "Same Day"}
        for mode in expected_modes:
            self.assertIn(mode, self.sales_summary)

    def test_total_sales_expected_segments_exist(self):
        #Known segments from the dataset should appear as inner keys
        expected_segments = {"Consumer", "Corporate", "Home Office"}
        for seg in expected_segments:
            found = any(seg in seg_dict for seg_dict in self.sales_summary.values())
            self.assertTrue(found, f"{seg} segment missing in output")

    def test_total_sales_skips_incomplete_rows(self):
        #Rows missing Ship Mode or Segment should not appear in the result
        self.assertNotIn("", self.sales_summary)
        for seg_dict in self.sales_summary.values():
            self.assertNotIn("", seg_dict)

    def test_total_sales_empty_input_returns_empty_dict(self):
        #When given an empty dataset, the function should return an empty dictionary
        self.assertEqual(total_sales_by_shipmode_and_segment([]), {})

#more specific for testfile.csv (expected output)
    def test_avg_discount_expected_output(self):
        expected = {
            'Office Supplies': 0.57,
            'Technology': 20.0,
            'Furniture': 11.59
        }
        self.assertEqual(self.avg_disc, expected)
    
    def test_total_sales_expected_output(self):
        expected = {
            'Standard Class': {'Consumer': 808.58, 'Corporate': 19.46},
            'Second Class': {'Consumer': 300.26, 'Home Office': 600.56},
            'Same Day': {'Corporate': 1043.92},
            'First Class': {'Corporate': 668.54}
        }
        self.assertEqual(self.sales_summary, expected)

#main
def main():
    d = load_superstore("SampleSuperstore.csv")
    avg_disc = avg_discount_by_category(d)
    sales_by_mode_seg = total_sales_by_shipmode_and_segment(d)
    write_results_to_csv(avg_disc, sales_by_mode_seg, "superstore_analysis.txt")
    print("Created superstore_analysis.txt") #make txt file

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2) #learned from discussion work