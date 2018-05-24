import React, { Component } from 'react';

import { Title } from './components/Title';
import { Divider } from './components/Divider';
import { ReportUploader } from './components/ReportUploader';
import { PayrollReport } from './components/PayrollReport';

class App extends Component {
  render() {
    return (
      <div className="container">
        <Title />
        <Divider />
        <ReportUploader />
        <Divider />
        <PayrollReport />
      </div>
    );
  }
}

export default App;
