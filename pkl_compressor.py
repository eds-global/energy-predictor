import zipfile

with zipfile.ZipFile('database/energy_prediction_model.pkl.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('database/energy_prediction_model.pkl', arcname='database/energy_prediction_model.pkl')
