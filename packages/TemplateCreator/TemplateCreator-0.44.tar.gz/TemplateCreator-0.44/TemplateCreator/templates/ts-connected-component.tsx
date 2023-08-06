import React, { Dispatch } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { StartLoaderAction, StopLoaderAction } from '../../../common/state/general/general.actions';
import { StyledContainer } from './{{ folder_name }}.styles';
import { RootState } from '../../../common/models';

export interface {{ component_name }}Props {

}

const {{ component_name }}: React.SFC<{{ component_name }}Props> = (props) => {
  return (
    <StyledContainer>{{ component_name }}</StyledContainer>
  );
}

const mapStateToProps = (state: RootState) => {
  const { general } = state.view;
  return {
    isLoading: general.loading
  };
};

const mapDispatchToProps = (dispatch: Dispatch<RootState>) => {
  return {
    startLoader: bindActionCreators(StartLoaderAction, dispatch),
    stopLoader: bindActionCreators(StopLoaderAction, dispatch)
  };
};

export default connect(
    mapStateToProps,
    mapDispatchToProps
)({{ component_name }});
