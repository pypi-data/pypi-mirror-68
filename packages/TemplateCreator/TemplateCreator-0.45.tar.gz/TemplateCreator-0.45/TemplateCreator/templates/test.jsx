import React from 'react';
import { mount } from 'enzyme';
import { {{ component_name }} } from '../../';

describe('{{ component_name }}', () => {
  let wrapper;

  const component = (<{{ component_name }} />);

  beforeEach(() => {
    wrapper = mount(component);
  });

  it('test', () => {

  });
});
