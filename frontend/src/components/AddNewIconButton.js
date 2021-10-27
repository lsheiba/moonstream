import React, { useContext } from "react";
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuGroup,
  MenuDivider,
  IconButton,
  chakra,
} from "@chakra-ui/react";
import { PlusSquareIcon } from "@chakra-ui/icons";
import UIContext from "../core/providers/UIProvider/context";
import ModalContext from "../core/providers/ModalProvider/context";

import {
  DRAWER_TYPES,
  MODAL_TYPES,
} from "../core/providers/ModalProvider/constants";

const AddNewIconButton = (props) => {
  const ui = useContext(UIContext);
  const modal = useContext(ModalContext);

  return (
    <Menu>
      <MenuButton
        {...props}
        as={IconButton}
        // onClick={ui.addNewDrawerState.onOpen}
        aria-label="Account menu"
        icon={<PlusSquareIcon />}
        // variant="outline"
        color="gray.100"
      />
      <MenuList
        zIndex="dropdown"
        width={["100vw", "100vw", "18rem", "20rem", "22rem", "24rem"]}
        borderRadius={0}
      >
        <MenuGroup>
          <MenuItem
            onClick={() => modal.toggleDrawer(DRAWER_TYPES.NEW_DASHBOARD)}
          >
            New Dashboard...
          </MenuItem>
          <MenuItem
            onClick={() => modal.toggleModal(MODAL_TYPES.NEW_SUBSCRIPTON)}
          >
            New Subscription...
          </MenuItem>

          {ui.isInDashboard && <MenuItem>New report...</MenuItem>}
        </MenuGroup>
        <MenuDivider />
      </MenuList>
    </Menu>
  );
};

const ChakraAddNewIconButton = chakra(AddNewIconButton);

export default ChakraAddNewIconButton;
