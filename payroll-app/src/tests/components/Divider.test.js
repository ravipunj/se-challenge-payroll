import React from 'react';
import { mount } from 'enzyme';

import { Divider } from '../../components/Divider';

describe('Divider', () => {
  it('matches snapshot', () => {
    expect(mount(<Divider/>)).toMatchSnapshot();
  });
});