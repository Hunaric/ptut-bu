import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThemeToggleTwoComponent } from './theme-toggle-two.component';

describe('ThemeToggleTwoComponent', () => {
  let component: ThemeToggleTwoComponent;
  let fixture: ComponentFixture<ThemeToggleTwoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ThemeToggleTwoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ThemeToggleTwoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
