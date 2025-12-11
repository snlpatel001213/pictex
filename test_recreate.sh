#!/bin/bash
# Test script for recreate_from_json.py

# 1. Create Sample JSON
cat > test_metadata.json <<EOF
{
  "base_image": "",
  "elements": [
    {
      "type": "text",
      "content": "Hello {child_name}, {gender}. He is a good boy. Him logic check.",
      "x": "10%",
      "y": "10%",
      "font_size": "5%",
      "color": "#FF0000"
    },
     {
      "type": "text",
      "content": "His toy. It is his.",
      "x": "10%",
      "y": "30%",
      "font_size": "5%",
      "color": "#00FF00"
    }
  ]
}
EOF

echo "Created test_metadata.json"

# 2. Run Python Script (Male)
echo "Running for Male (Liam)..."
/Users/supatel/Documents/pictext/pictex/.venv/bin/python recreate_from_json.py test_metadata.json output_male.png --child-name "Liam" --gender "Male"

# 3. Run Python Script (Female)
echo "Running for Female (Emma)..."
/Users/supatel/Documents/pictext/pictex/.venv/bin/python recreate_from_json.py test_metadata.json output_female.png --child-name "Emma" --gender "Female"

echo "Done. Please check output_male.png and output_female.png"
