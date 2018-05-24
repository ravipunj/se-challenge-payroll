import React from 'react';
import { shallow } from 'enzyme';

import { PayrollReport } from '../../components/PayrollReport';

describe('PayrollReport', () => {
  it('matches snapshot', () => {
    expect(shallow(<PayrollReport/>)).toMatchSnapshot();
  });
});