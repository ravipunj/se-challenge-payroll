import React from 'react';
import { shallow } from 'enzyme';

import { ReportUploader } from '../../components/ReportUploader';

describe('ReportUploader', () => {
  it('matches snapshot', () => {
    expect(shallow(<ReportUploader/>)).toMatchSnapshot();
  });
});