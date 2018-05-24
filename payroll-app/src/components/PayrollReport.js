import React from 'react';
import axios from 'axios';

export class PayrollReport extends React.Component {
  constructor() {
    super();
    this.state = {payroll_report: []};
  }
  componentDidMount() {
    axios.get('/payroll_report').then(response => {
      if(response.status === 200) {
        this.setState({payroll_report: response.data})
      }
    });
  }
  render() {
    return (
      <div className="row">
        <div className="column">
          <table>
            <thead>
              <tr>
                <th>Employee ID</th>
                <th>Pay Period</th>
                <th>Amount Paid</th>
              </tr>
            </thead>
            <tbody>
              {this.state.payroll_report.map((entry,idx) => (
                <tr key={idx}>
                  <td>{entry.employee_id}</td>
                  <td>{entry.pay_period}</td>
                  <td>{entry.amount_paid}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
}