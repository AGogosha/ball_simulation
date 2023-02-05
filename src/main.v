module main

import math
import math.vec as mv
import os

fn main() {
	delt_t := f32(0.0001)
	r := f64(1)
	pos_init := mv.vec3[f64](-0.5 * r, 0, 0)
	init_vel := [mv.vec3[f64](0, 1.5, 0), mv.vec3[f64](0, 0.8, 0),
		mv.vec3[f64](0, 0.45, 0), mv.vec3[f64](0, 0.328, 0), mv.vec3[f64](0.33234, 0.33234,
			0),
		mv.vec3[f64](0.200111, 0.200111, 0)]
	init_durations := [f64(0.86), 2.9, 17.3, 5, 3.83, 3.3]
	omega := mv.vec3[f64](0, 0, 1)
	//mut path := [][]mv.Vec3[f64]{cap: init_vel.len}
	mut threads := []thread []mv.Vec3[f64]{cap: init_vel.len}
	for i, vel in init_vel {
		threads << spawn cal_path(pos_init, vel, omega, delt_t, init_durations[i])
		//path << cal_path(pos_init, vel, omega, delt_t, init_durations[i])
	}
	path := threads.wait()
	write_out(path)!
}

fn first_pos(zero_pos mv.Vec3[f64], zero_vel mv.Vec3[f64], zero_acel mv.Vec3[f64], timestep f32) mv.Vec3[f64] {
	return zero_pos + zero_vel.mul_scalar(timestep) +
		zero_acel.mul_scalar(math.powf(timestep, 2)).div_scalar(2)
}

fn next_pos(pos_cur mv.Vec3[f64], pos_prev mv.Vec3[f64], a_cur mv.Vec3[f64], timestep f32) mv.Vec3[f64] {
	return pos_cur.mul_scalar(2) - pos_prev + a_cur.mul_scalar(math.powf(timestep, 2))
}

fn cal_vel(cur_pos mv.Vec3[f64], prev_pos mv.Vec3[f64], timestep f32) mv.Vec3[f64] {
	return (cur_pos - prev_pos).div_scalar(timestep)
}

fn cal_accel(omega mv.Vec3[f64], pos mv.Vec3[f64], rad_vel mv.Vec3[f64]) mv.Vec3[f64] {
	mut tmp := (omega.cross(omega.cross(pos))).mul_scalar(-1) - (omega.cross(rad_vel).mul_scalar(2))
	return tmp
}

fn cal_path(init_pos mv.Vec3[f64], init_vel mv.Vec3[f64], omega mv.Vec3[f64], timestep f32, duration f64) []mv.Vec3[f64] {
	a0 := cal_accel(omega, init_pos, init_vel)
	loop_length := int((duration + timestep) / timestep)
	mut path := []mv.Vec3[f64]{cap: loop_length}
	path << init_pos
	path << first_pos(init_pos, init_vel, a0, timestep)
	for _ in 0 .. loop_length {
		cur_pos := path.last()
		// println(cur_pos)
		prev_pos := path[path.len - 2]
		// println(prev_pos)
		cur_vel := cal_vel(cur_pos, prev_pos, timestep)
		cur_accel := cal_accel(omega, cur_pos, cur_vel)
		path << next_pos(cur_pos, prev_pos, cur_accel, timestep)
	}

	return path
}

fn write_out(paths [][]mv.Vec3[f64]) !int {
	for i, path in paths {
		mut f := os.create('broke out ${i}.csv')!
		f.writeln('x,y')!
		defer {
			f.close()
		}
		for vec in path {
			f.writeln('${vec.x},${vec.y}')!
		}
	}
	return 0
}
