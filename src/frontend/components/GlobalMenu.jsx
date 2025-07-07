// src/components/GlobalMenu.jsx
import React, { useState } from 'react';
import { AppBar, Toolbar, Typography, IconButton, Drawer, List, ListItem, ListItemText } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { useNavigate } from 'react-router-dom';

export default function GlobalMenu() {
    const [open, setOpen] = useState(false);
    const navigate = useNavigate();

    const toggleDrawer = () => setOpen(!open);

    const menuItems = [
        { text: 'Organizations', route: '/organizations' },
        { text: 'Practices', route: '/practices' },
        { text: 'Roles', route: '/roles' },
        { text: 'Questions', route: '/questions' }
    ];

    return (
        <>
            <AppBar position="static">
                <Toolbar>
                    <IconButton edge="start" color="inherit" onClick={toggleDrawer}>
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6">Audit App</Typography>
                </Toolbar>
            </AppBar>
            <Drawer anchor="left" open={open} onClose={toggleDrawer}>
                <List>
                    {menuItems.map((item) => (
                        <ListItem
                            button
                            key={item.text}
                            onClick={() => {
                                navigate(item.route);
                                toggleDrawer();
                            }}
                        >
                            <ListItemText primary={item.text} />
                        </ListItem>
                    ))}
                </List>
            </Drawer>
        </>
    );
}