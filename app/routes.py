from flask import Blueprint, request, jsonify
from app.models import Website
from app.tool import db

main = Blueprint('main', __name__)

@main.route('/api/websites', methods = ['GET'])
def get_websites():
    websites = Website.query.all()
    result = []
    for site in websites:
        result.append({
            "id": site.id,
            "url": site.url,
            "status": site.status,
            "last_checked": site.last_checked.strftime('%Y-%m-%d %H:%M:%S') if site.last_checked else None
        })
    return jsonify(result)

@main.route('/api/websites', methods=['POST'])
def add_website():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error" : "URL is required "}), 400
    
    new_site = Website(
        url = url,
        status = 'unknow',
        user_id = 1
    )
    db.session.add(new_site)
    db.session.commit()
    return jsonify({"message" : "Website added"}),201

@main.route('/api/websites/<int:site_id>', methods = ['PUT'])
def update_website(site_id):
    data = request.json
    site = Website.query.get(site_id)
    if not site:
        return jsonify({"error": "Website not Found"}), 404
    
    site.url = data.get('url', site.url)
    db.session.commit()
    return jsonify({"message" : "Website updated"}), 200

@main.route('/api/websites/<int:site_id>', methods = ['DELETE'])
def delete_website(site_id):
    site = Website.query.get(site_id)
    if not site:
        return jsonify({"error": "Website not found"}), 404
    db.session.delete(site)
    db.session.commit()
    return jsonify({"message" : "Website deleted"}), 200


