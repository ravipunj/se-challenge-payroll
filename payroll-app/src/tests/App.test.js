import React from 'react';
import {mount} from 'enzyme';

import App from '../App';

describe('App', () => {
  it('matches snapshot', () => {
    expect(mount(<App />)).toMatchSnapshot();
  });
});