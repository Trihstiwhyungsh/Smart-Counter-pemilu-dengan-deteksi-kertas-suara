import json
from app import db
from app.models import tps_model

# def add_admin():
#     admin = user_model.Users("adepriyantowidies@gmail.com", "Widies Ade", \
#         "Priyanto", "Male", "4837feeb-5e9a-4493-9114-507792ca2959")
#     admin.set_role("Admin")
#     admin.set_password("admin123")
#     db.session.add(admin)
#     db.session.commit()
#     db.session.close()

def main():
    all_tps = []
    with open("tps.json", encoding='UTF-8') as json_data:
        data_tps = json.load(json_data)
        for tps in data_tps:
            all_tps.append(tps_model.TPS(
                nama_tps=tps['nama_tps'],
                alamat=tps['alamat'],
                suara_sah=tps['suara_sah'],
                suara_tidak_sah=tps['suara_tidak_sah']))

    db.drop_all()
    db.create_all()
    db.session.bulk_save_objects(all_tps)
    db.session.commit()
    db.session.close()
    # add_admin()

if __name__ == "__main__":
    main()
