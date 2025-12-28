// permission.model.ts
export interface Permission {
  id: number;
  name: string;          // loan:create, loan:manage, etc.
  description?: string;
}

export interface MyPermissions {
  name: string;          // loan:create, loan:manage, etc.
}
