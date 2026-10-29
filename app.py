# Ponto de entrada: cria o app, junta o layout e os callbacks e liga o servidor.
# No Render: gunicorn app:server

import os
from dash import Dash

from layout import layout
import callbacks  # noqa: F401  (importar já registra os callbacks)


app = Dash(__name__, title="Quadro de Medalhas Olímpicas")
server = app.server
app.layout = layout


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
