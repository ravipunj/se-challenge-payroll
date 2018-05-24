import React from 'react';
import { mount } from 'enzyme';

import { ReportUploader } from '../../components/ReportUploader';

describe('ReportUploader', () => {
  it('matches snapshot', () => {
    expect(mount(<ReportUploader/>)).toMatchSnapshot();
  });
});