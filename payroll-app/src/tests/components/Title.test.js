import React from 'react';
import { mount } from 'enzyme';

import { Title } from '../../components/Title';

describe('Title', () => {
  it('matches snapshot', () => {
    expect(mount(<Title/>)).toMatchSnapshot();
  });
});