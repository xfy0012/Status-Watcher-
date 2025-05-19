# Importing necessary modules from Flask
from flask import Blueprint, request, jsonify
# Importing the Website model
from app.models import Website
# Importing the database instance
from app.tool import db

# Creating a Blueprint named 'main' to group related routes
main = Blueprint('main', __name__)

# Route to get all websites from the database
@main.route('/api/websites', methods = ['GET'])
def get_websites():
    # Query all website entries
    websites = Website.query.all()
    result = []
    for site in websites:
        # Format the response with website details
        result.append({
            "id": site.id,
            "url": site.url,
            "status": site.status,
            "last_checked": site.last_checked.strftime('%Y-%m-%d %H:%M:%S') if site.last_checked else None
        })
    # Return the list of websites in JSON format
    return jsonify(result)

# Route to add a new website entry
@main.route('/api/websites', methods=['POST'])
def add_website():
    # Retrieve the JSON data sent in the request body
    data = request.json
    url = data.get('url')
    # Return an error if URL is not provided
    if not url:
        return jsonify({"error" : "URL is required "}), 400
    
    # For now, user_id is hardcoded as 1 for all new websites.
    # This is a placeholder for future user system expansion.
    new_site = Website(
        url = url,
        status = 'unknown',  # Use the correct spelling for consistency
        user_id = 1
    )
    # Add and commit the new site to the database
    db.session.add(new_site)
    db.session.commit()
    return jsonify({"message" : "Website added"}),201

# Route to update an existing website entry by ID
@main.route('/api/websites/<int:site_id>', methods = ['PUT'])
def update_website(site_id):
    # Get request data
    data = request.json
    # Fetch the target website by ID
    site = Website.query.get(site_id)
    # If no such site is found, return an error
    if not site:
        return jsonify({"error": "Website not Found"}), 404
    
    # Update URL and status if provided in the request
    site.url = data.get('url', site.url)

    # Commit the changes to the database
    db.session.commit()
    return jsonify({"message" : "Website updated"}), 200

# Route to delete a website by its ID
@main.route('/api/websites/<int:site_id>', methods = ['DELETE'])
def delete_website(site_id):
    # Query the website with the given ID from the database
    site = Website.query.get(site_id)
    # If the site does not exist, return a 404 error
    if not site:
        return jsonify({"error": "Website not found"}), 404
    
    # Delete the website entry from the database
    db.session.delete(site)
    db.session.commit()

     # Return a success message
    return jsonify({"message" : "Website deleted"}), 200


