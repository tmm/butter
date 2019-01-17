import React from "react";
import { Box, Button } from "../../../../components";
import { BooleanField } from "../../../../components/core/components/form/BooleanField";

interface Props {
    allSelected: boolean;
    anySelected: boolean;
    handleOnChange: Function;
    handleDelete: Function;
}

export default class Header extends React.Component<Props> {
    onChange = () => {
        this.props.handleOnChange();
    };

    onClickDelete = () => {
        this.props.handleDelete();
    };

    render() {
        const { allSelected, anySelected } = this.props;
        return (
            <Box
                alignItems={Box.AlignItems.Center}
                css={`
                    height: 53px;
                `}
                display={Box.Display.Flex}
                ph={2}
                pb={2}
            >
                <Box mr={2.5} pt={0.35}>
                    <BooleanField
                        checked={anySelected || allSelected}
                        deselect={anySelected && !allSelected}
                        onChange={this.onChange}
                    />
                </Box>
                {anySelected && (
                    <Box mr={2}>
                        <Button
                            color={Button.Color.Secondary}
                            onClick={this.onClickDelete}
                        >
                            Delete
                        </Button>
                    </Box>
                )}
            </Box>
        );
    }
}