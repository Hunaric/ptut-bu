import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AppBackdropComponent } from './app-backdrop.component';

describe('AppBackdropComponent', () => {
  let component: AppBackdropComponent;
  let fixture: ComponentFixture<AppBackdropComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppBackdropComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AppBackdropComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
