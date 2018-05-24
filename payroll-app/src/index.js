import React from 'react';
import ReactDOM from 'react-dom';
import 'milligram';
import axios from 'axios';

import App from './App';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();

axios.defaults.baseURL = "http://0.0.0.0:8000";
