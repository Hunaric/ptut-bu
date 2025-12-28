// user.model.ts

import { Permission } from "./permission";
import { Role } from "./role";

export interface User {
  id: string;           // UUID
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  role?: Role;
  permissions?: Permission[];
}

export interface Me {
  username: string;           // UUID
  email: string;
  role?: Role;
  permissions?: Permission[];
}
