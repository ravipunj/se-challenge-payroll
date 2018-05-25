import React from 'react';
import { shallow } from 'enzyme';

import { Title } from '../../components/Title';

describe('Title', () => {
  it('matches snapshot', () => {
    expect(shallow(<Title/>)).toMatchSnapshot();
  });
});