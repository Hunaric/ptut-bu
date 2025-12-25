// user.model.ts
import { Role } from './role.model';
import { Permission } from './permission.model';

export interface User {
  id: string;           // UUID
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  role?: Role;
  permissions?: Permission[];
}
