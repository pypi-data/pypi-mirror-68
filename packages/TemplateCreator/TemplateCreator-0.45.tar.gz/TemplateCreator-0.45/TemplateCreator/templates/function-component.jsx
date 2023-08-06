import React from 'react';
import PropTypes from 'prop-types';
import { ThemeProvider } from 'styled-components';
import StyledContainer from './{{ folder_name }}.styles';

const {{ component_name }} = (props) => {
  return (
    <ThemeProvider theme={{ '{' }}{{ component_name }}.theme}>
      <StyledContainer>
        {{ component_name }}
      </StyledContainer>
    </ThemeProvider>
  );
};

{{ component_name }}.propTypes = {

};

{{ component_name }}.defaultProps = {

};

export default {{ component_name }};
