import React from 'react';
import axios from 'axios';

export class ReportUploader extends React.Component {
  constructor() {
    super();
    this.state = {submitDisabled: true};
    this.onSubmit = this.onSubmit.bind(this);
    this.onFileChanged = this.onFileChanged.bind(this);
  }
  onSubmit(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("report", this.fileInput.files[0]);
    axios.post("/payroll_csv", formData, {headers: {"Content-Type": "multipart/form-data"}});
  }
  onFileChanged() {
    this.setState({submitDisabled: this.fileInput.files.length === 0});
  }
  render() {
    return (
      <div className="row">
        <div className="column">
          <form onSubmit={this.onSubmit} style={style}>
            <fieldset>
              <h4>Upload Payroll Report CSV</h4>
              <input type="file" id="reportFile" ref={input => {this.fileInput = input}} onChange={this.onFileChanged}/>
              <input type="submit" className="button" value="Upload" disabled={this.state.submitDisabled}/>
            </fieldset>
          </form>
        </div>
      </div>
    );
  }
}

const style = {
  textAlign: 'center'
}