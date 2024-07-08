'use client';

import * as React from 'react';
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
    '& .MuiDialogContent-root': {
        padding: theme.spacing(2),
    },
    '& .MuiDialogActions-root': {
        padding: theme.spacing(1),
    },
}));

export type CustomDialogProps = {
    isOpen: boolean;
}

function CustomDialog(props: CustomDialogProps) {
    const {
        isOpen,
    } = props;

    return (
        <React.Fragment>
            <BootstrapDialog
                aria-labelledby="customized-dialog-title"
                open={isOpen}
            >
                <DialogContent className="flex justify-center items-center w-[64px] h-[64px]">
                    <Box sx={{ display: 'flex' }}>
                        <CircularProgress color="primary" size="32px"/>
                    </Box>
                </DialogContent>
            </BootstrapDialog>
        </React.Fragment>
    );
}

export default CustomDialog;
