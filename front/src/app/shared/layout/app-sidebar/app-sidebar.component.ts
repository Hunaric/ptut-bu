import { CommonModule } from '@angular/common';
import { Component, ElementRef, QueryList, ViewChildren, ChangeDetectorRef } from '@angular/core';
import { SidebarService } from '../../services/sidebar.service';
import { NavigationEnd, Router, RouterModule } from '@angular/router';
import { SafeHtmlPipe } from '../../pipe/safe-html.pipe';
import { combineLatest, Subscription } from 'rxjs';
import { AuthService } from '../../../services/auth.service';
import { MyPermissions } from '../../../interfaces/permission';

type NavItem = {
  name: string;
  icon: string;
  path?: string;
  new?: boolean;
  noAdminPrefix?: boolean; // <-- nouveau champ
  subItems?: { name: string; path: string; pro?: boolean; new?: boolean, noAdminPrefix?: boolean; }[];
};

@Component({
  selector: 'app-sidebar',
  imports: [
    CommonModule,
    RouterModule,
    SafeHtmlPipe,
    // SidebarWidgetComponent
  ],
  templateUrl: './app-sidebar.component.html',
})
export class AppSidebarComponent {

  basePrefix = '';
  navItems: NavItem[] = [];

  openSubmenu: string | null | number = null;
  subMenuHeights: { [key: string]: number } = {};
  @ViewChildren('subMenu') subMenuRefs!: QueryList<ElementRef>;

  readonly isExpanded$;
  readonly isMobileOpen$;
  readonly isHovered$;
  permissions: string[] = [];

  private subscription: Subscription = new Subscription();

  constructor(
    public sidebarService: SidebarService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    public authService: AuthService
  ) {
    this.isExpanded$ = this.sidebarService.isExpanded$;
    this.isMobileOpen$ = this.sidebarService.isMobileOpen$;
    this.isHovered$ = this.sidebarService.isHovered$;

    // Si l’URL actuelle contient "/admin", on ajoute le préfixe automatiquement
    if (this.router.url.startsWith('/admin')) {
      this.basePrefix = '/admin';
    }
  }

  ngOnInit() {
    // Subscribe to router events
    this.subscription.add(
      this.router.events.subscribe(event => {
        if (event instanceof NavigationEnd) {
          this.setActiveMenuFromRoute(this.router.url);
        }
      })
    );

    // Subscribe to combined observables to close submenus when all are false
    this.subscription.add(
      combineLatest([this.isExpanded$, this.isMobileOpen$, this.isHovered$]).subscribe(
        ([isExpanded, isMobileOpen, isHovered]) => {
          if (!isExpanded && !isMobileOpen && !isHovered) {
            // this.openSubmenu = null;
            // this.savedSubMenuHeights = { ...this.subMenuHeights };
            // this.subMenuHeights = {};
            this.cdr.detectChanges();
          } else {
            // Restore saved heights when reopening
            // this.subMenuHeights = { ...this.savedSubMenuHeights };
            // this.cdr.detectChanges();
          }
        }
      )
    );

    // Initial load
    this.setActiveMenuFromRoute(this.router.url);

   this.permissions = this.authService.getPermissions() || [];
  //  console.log(this.permissions);

  this.navItems = this.buildNavItems();
   
  }

  ngOnDestroy() {
    // Clean up subscriptions
    this.subscription.unsubscribe();
  }

  isActive(path: string): boolean {
    return this.router.url === path;
  }

  toggleSubmenu(section: string, index: number) {
    const key = `${section}-${index}`;

    if (this.openSubmenu === key) {
      this.openSubmenu = null;
      this.subMenuHeights[key] = 0;
    } else {
      this.openSubmenu = key;

      setTimeout(() => {
        const el = document.getElementById(key);
        if (el) {
          this.subMenuHeights[key] = el.scrollHeight;
          this.cdr.detectChanges(); // Ensure UI updates
        }
      });
    }
  }

  onSidebarMouseEnter() {
    this.isExpanded$.subscribe(expanded => {
      if (!expanded) {
        this.sidebarService.setHovered(true);
      }
    }).unsubscribe();
  }

  private setActiveMenuFromRoute(currentUrl: string) {
    const menuGroups = [
      { items: this.navItems, prefix: 'main' },
      { items: this.othersItems, prefix: 'others' },
    ];

    menuGroups.forEach(group => {
      group.items.forEach((nav, i) => {
        if (nav.subItems) {
          nav.subItems.forEach(subItem => {
            if (currentUrl === subItem.path) {
              const key = `${group.prefix}-${i}`;
              this.openSubmenu = key;

              setTimeout(() => {
                const el = document.getElementById(key);
                if (el) {
                  this.subMenuHeights[key] = el.scrollHeight;
                  this.cdr.detectChanges(); // Ensure UI updates
                }
              });
            }
          });
        }
      });
    });
  }

  onSubmenuClick() {
    // console.log('click submenu');
    this.isMobileOpen$.subscribe(isMobile => {
      if (isMobile) {
        this.sidebarService.setMobileOpen(false);
      }
    }).unsubscribe();
  }  

  // Combine intelligemment le prefixe avec le path
  getFullPath(path: string, noAdminPrefix?: boolean): string {
  if (!path) return this.basePrefix;
  if (path.startsWith('/')) path = path.substring(1); // enlever le premier /
  return noAdminPrefix ? `/${path}` : `${this.basePrefix}/${path}`;
}


  // Main nav items
  private buildNavItems(): NavItem[] {
  return  [
    {
      icon: `<svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M5.5 3.25C4.25736 3.25 3.25 4.25736 3.25 5.5V8.99998C3.25 10.2426 4.25736 11.25 5.5 11.25H9C10.2426 11.25 11.25 10.2426 11.25 8.99998V5.5C11.25 4.25736 10.2426 3.25 9 3.25H5.5ZM4.75 5.5C4.75 5.08579 5.08579 4.75 5.5 4.75H9C9.41421 4.75 9.75 5.08579 9.75 5.5V8.99998C9.75 9.41419 9.41421 9.74998 9 9.74998H5.5C5.08579 9.74998 4.75 9.41419 4.75 8.99998V5.5ZM5.5 12.75C4.25736 12.75 3.25 13.7574 3.25 15V18.5C3.25 19.7426 4.25736 20.75 5.5 20.75H9C10.2426 20.75 11.25 19.7427 11.25 18.5V15C11.25 13.7574 10.2426 12.75 9 12.75H5.5ZM4.75 15C4.75 14.5858 5.08579 14.25 5.5 14.25H9C9.41421 14.25 9.75 14.5858 9.75 15V18.5C9.75 18.9142 9.41421 19.25 9 19.25H5.5C5.08579 19.25 4.75 18.9142 4.75 18.5V15ZM12.75 5.5C12.75 4.25736 13.7574 3.25 15 3.25H18.5C19.7426 3.25 20.75 4.25736 20.75 5.5V8.99998C20.75 10.2426 19.7426 11.25 18.5 11.25H15C13.7574 11.25 12.75 10.2426 12.75 8.99998V5.5ZM15 4.75C14.5858 4.75 14.25 5.08579 14.25 5.5V8.99998C14.25 9.41419 14.5858 9.74998 15 9.74998H18.5C18.9142 9.74998 19.25 9.41419 19.25 8.99998V5.5C19.25 5.08579 18.9142 4.75 18.5 4.75H15ZM15 12.75C13.7574 12.75 12.75 13.7574 12.75 15V18.5C12.75 19.7426 13.7574 20.75 15 20.75H18.5C19.7426 20.75 20.75 19.7427 20.75 18.5V15C20.75 13.7574 19.7426 12.75 18.5 12.75H15ZM14.25 15C14.25 14.5858 14.5858 14.25 15 14.25H18.5C18.9142 14.25 19.25 14.5858 19.25 15V18.5C19.25 18.9142 18.9142 19.25 18.5 19.25H15C14.5858 19.25 14.25 18.9142 14.25 18.5V15Z" fill="currentColor"></path></svg>`,
      name: "Accueil",
      subItems: [
        { name: "Tableau de bord", path: "/" },
      ...(this.permissions.includes("loan:manage")
        ? [{ name: "Creer un livre", path: "/crud-books", pro: true }]
        : [{ name: "Mes recommandations", path: "/recommendation", pro: false }]),
      ]
    },
    {
      icon: `<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M8 2C8.41421 2 8.75 2.33579 8.75 2.75V3.75H15.25V2.75C15.25 2.33579 15.5858 2 16 2C16.4142 2 16.75 2.33579 16.75 2.75V3.75H18.5C19.7426 3.75 20.75 4.75736 20.75 6V9V19C20.75 20.2426 19.7426 21.25 18.5 21.25H5.5C4.25736 21.25 3.25 20.2426 3.25 19V9V6C3.25 4.75736 4.25736 3.75 5.5 3.75H7.25V2.75C7.25 2.33579 7.58579 2 8 2ZM8 5.25H5.5C5.08579 5.25 4.75 5.58579 4.75 6V8.25H19.25V6C19.25 5.58579 18.9142 5.25 18.5 5.25H16H8ZM19.25 9.75H4.75V19C4.75 19.4142 5.08579 19.75 5.5 19.75H18.5C18.9142 19.75 19.25 19.4142 19.25 19V9.75Z" fill="currentColor"></path></svg>`,
      name: "Calendrier des retours",
      path: "/calendar",
    },
    
    {
      name: "Bibliotheque",
      icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 128 128" style="enable-background:new 0 0 128 128" xml:space="preserve"><path d="M110.6 38.3H106v-3.5c0-1-.8-1.7-1.7-1.8H70.8c-2.7 0-5.2 1.2-6.8 3.3-1.6-2.1-4.1-3.3-6.8-3.3H23.7c-1 0-1.7.8-1.7 1.8v3.5h-4.6c-1 0-1.8.8-1.8 1.8v57c0 1 .8 1.7 1.8 1.8h93.1c1 0 1.7-.8 1.8-1.8V40c0-.9-.8-1.7-1.7-1.7zm-39.8-1.8h31.7v51.9H70.8c-2.9 0-4.6 1.4-5 1.6V41.6c0-.4 0-.7-.1-1.1.5-2.2 2.6-4 5.1-4zm-45.3 0h31.7c2.6 0 4.7 1.9 5 4.1 0 .4-.1.7-.1 1.1V90c-.3-.1-2.1-1.6-5-1.6H25.5V36.5zm-6.3 5.3H22v48.3c0 1 .8 1.8 1.8 1.8h33.5c2 0 3.9 1.1 4.8 3.4H19.2V41.8zm89.6 53.5H66c.8-2.2 2.8-3.4 4.8-3.4h33.5c1 0 1.8-.8 1.8-1.8V41.8h2.8l-.1 53.5z"/><path d="M32.7 50h22.5c1 0 1.8-.8 1.8-1.8s-.8-1.8-1.8-1.8H32.7c-1 0-1.8.8-1.8 1.8s.8 1.8 1.8 1.8zM32.7 59.3h22.5c1 0 1.8-.8 1.8-1.8s-.8-1.8-1.8-1.8H32.7c-1 0-1.8.8-1.8 1.8s.8 1.8 1.8 1.8zM32.7 68.7h22.5c1 0 1.8-.8 1.8-1.8s-.8-1.8-1.8-1.8H32.7c-1 0-1.8.8-1.8 1.8s.8 1.8 1.8 1.8zM32.7 78h22.5c1 0 1.8-.8 1.8-1.8s-.8-1.8-1.8-1.8H32.7c-1 0-1.8.8-1.8 1.8s.8 1.8 1.8 1.8zM72.8 50h22.5c1 0 1.8-.8 1.8-1.8s-.8-1.8-1.8-1.8H72.8c-1 0-1.8.8-1.8 1.8s.9 1.8 1.8 1.8zM72.8 59.3h22.5c1 0 1.8-.8 1.8-1.8s-.8-1.8-1.8-1.8H72.8c-1 0-1.8.8-1.8 1.8s.9 1.8 1.8 1.8zM72.8 68.7h22.5c1 0 1.8-.8 1.8-1.8s-.8-1.8-1.8-1.8H72.8c-1 0-1.8.8-1.8 1.8s.9 1.8 1.8 1.8zM72.8 78h22.5c1 0 1.8-.8 1.8-1.8s-.8-1.8-1.8-1.8H72.8c-1 0-1.8.8-1.8 1.8s.9 1.8 1.8 1.8z" fill="currentColor"/></svg>`,
      subItems: [
        { name: "Livres", path: "/books", pro: false },
        ...(this.permissions.includes("loan:manage")
        ? [{ name: "Assigner permission", path: "/permission", pro: true }]
        : [{ name: "Emprunts", path: "/my-loans", pro: false }]),
        ...(this.permissions.includes("loan:manage") || this.permissions.includes("loan:view")
        ? [{ name: "Voir emprunts", path: "/loan-list", pro: true }]
        : []),
      ],
    },
  ];
}
  // Others nav items
  othersItems: NavItem[] = [
    {
      icon: `<svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 3.5C7.30558 3.5 3.5 7.30558 3.5 12C3.5 14.1526 4.3002 16.1184 5.61936 17.616C6.17279 15.3096 8.24852 13.5955 10.7246 13.5955H13.2746C15.7509 13.5955 17.8268 15.31 18.38 17.6167C19.6996 16.119 20.5 14.153 20.5 12C20.5 7.30558 16.6944 3.5 12 3.5ZM17.0246 18.8566V18.8455C17.0246 16.7744 15.3457 15.0955 13.2746 15.0955H10.7246C8.65354 15.0955 6.97461 16.7744 6.97461 18.8455V18.856C8.38223 19.8895 10.1198 20.5 12 20.5C13.8798 20.5 15.6171 19.8898 17.0246 18.8566ZM2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12ZM11.9991 7.25C10.8847 7.25 9.98126 8.15342 9.98126 9.26784C9.98126 10.3823 10.8847 11.2857 11.9991 11.2857C13.1135 11.2857 14.0169 10.3823 14.0169 9.26784C14.0169 8.15342 13.1135 7.25 11.9991 7.25ZM8.48126 9.26784C8.48126 7.32499 10.0563 5.75 11.9991 5.75C13.9419 5.75 15.5169 7.32499 15.5169 9.26784C15.5169 11.2107 13.9419 12.7857 11.9991 12.7857C10.0563 12.7857 8.48126 11.2107 8.48126 9.26784Z" fill="currentColor"></path></svg>`,
      name: "Mon Profil",
      path: "/profile",
    },
    {
      name: "Parametres",
      icon: `<svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 128 128"><path d="M83.172 41.128a1.75 1.75 0 0 0-2.25 2.68A26.32 26.32 0 0 1 90.357 64a1.75 1.75 0 0 0 3.5 0 29.8 29.8 0 0 0-10.685-22.872z"/><path d="M64 40.143A23.857 23.857 0 1 0 87.857 64 23.884 23.884 0 0 0 64 40.143zm0 44.215A20.357 20.357 0 1 1 84.357 64 20.38 20.38 0 0 1 64 84.357z"/><path d="M122.55 54.882a1.751 1.751 0 0 0-1.73-1.482h-16.64a41.166 41.166 0 0 0-4.28-10.319l11.763-11.764a1.749 1.749 0 0 0 .176-2.27 59.2 59.2 0 0 0-12.887-12.89 1.753 1.753 0 0 0-2.27.176L84.919 28.1A41.166 41.166 0 0 0 74.6 23.819V7.18a1.751 1.751 0 0 0-1.482-1.73 59.968 59.968 0 0 0-18.236 0A1.751 1.751 0 0 0 53.4 7.18v16.64a41.166 41.166 0 0 0-10.319 4.28L31.317 16.333a1.751 1.751 0 0 0-2.27-.176 59.2 59.2 0 0 0-12.89 12.891 1.749 1.749 0 0 0 .176 2.27L28.1 43.081A41.166 41.166 0 0 0 23.819 53.4H7.18a1.751 1.751 0 0 0-1.73 1.482 59.72 59.72 0 0 0 0 18.236A1.751 1.751 0 0 0 7.18 74.6h16.64a41.166 41.166 0 0 0 4.28 10.319L16.333 96.683a1.749 1.749 0 0 0-.176 2.27 59.2 59.2 0 0 0 12.891 12.891 1.75 1.75 0 0 0 2.27-.176L43.081 99.9a41.166 41.166 0 0 0 10.319 4.281v16.64a1.751 1.751 0 0 0 1.481 1.729 59.72 59.72 0 0 0 18.236 0 1.751 1.751 0 0 0 1.483-1.73v-16.64a41.166 41.166 0 0 0 10.319-4.28l11.764 11.763a1.751 1.751 0 0 0 2.27.176 59.2 59.2 0 0 0 12.891-12.891 1.749 1.749 0 0 0-.176-2.27L99.9 84.919a41.166 41.166 0 0 0 4.281-10.319h16.64a1.751 1.751 0 0 0 1.729-1.481 59.72 59.72 0 0 0 0-18.236zM119.3 71.1h-16.492a1.751 1.751 0 0 0-1.707 1.362 37.675 37.675 0 0 1-4.886 11.79 1.751 1.751 0 0 0 .243 2.171l11.66 11.66a55.657 55.657 0 0 1-10.035 10.035l-11.66-11.66a1.752 1.752 0 0 0-2.171-.243 37.675 37.675 0 0 1-11.79 4.886 1.751 1.751 0 0 0-1.362 1.707V119.3a56.632 56.632 0 0 1-14.2 0v-16.492a1.751 1.751 0 0 0-1.362-1.707 37.675 37.675 0 0 1-11.79-4.886 1.749 1.749 0 0 0-2.171.243l-11.66 11.66a55.657 55.657 0 0 1-10.035-10.035l11.66-11.66a1.751 1.751 0 0 0 .243-2.171 37.675 37.675 0 0 1-4.885-11.79 1.751 1.751 0 0 0-1.708-1.362H8.7a56.327 56.327 0 0 1 0-14.2h16.492a1.751 1.751 0 0 0 1.708-1.362 37.675 37.675 0 0 1 4.886-11.79 1.751 1.751 0 0 0-.243-2.171l-11.66-11.66a55.657 55.657 0 0 1 10.034-10.035l11.66 11.66a1.75 1.75 0 0 0 2.171.243 37.675 37.675 0 0 1 11.79-4.885 1.751 1.751 0 0 0 1.362-1.708V8.7a56.632 56.632 0 0 1 14.2 0v16.492a1.751 1.751 0 0 0 1.362 1.708 37.675 37.675 0 0 1 11.79 4.886 1.752 1.752 0 0 0 2.171-.243l11.66-11.66a55.657 55.657 0 0 1 10.035 10.035l-11.66 11.66a1.751 1.751 0 0 0-.243 2.171 37.675 37.675 0 0 1 4.886 11.79 1.751 1.751 0 0 0 1.707 1.362H119.3a56.327 56.327 0 0 1 0 14.2z" fill="currentColor"/></svg>`,
      subItems: [
        // { name: "Mot de passe", path: "/password", pro: false },
        // { name: "Condition d'utilisation", path: "/conditions", pro: false },
        { name: "FAQ", path: "/faq", pro: false },
      ],
    },
  ];
  
}
